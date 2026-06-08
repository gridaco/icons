"""
Local LLM (ollama, vision) wrapper that turns a rendered icon PNG into a
one-line description and tags.

The prompt + JSON schema here are the *contract*. They are written to generalize
across vision models (not just the default). We request ollama structured output
(``format=<schema>``) at ``temperature=0`` for determinism, but not every model
honors ``format`` (the default gemma4 MLX runner ignores it and may wrap output
in markdown / refuse), so ``extract_json`` parses defensively and retries bump
the temperature to break a deterministic bad reply. See ollama/ollama#15260.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import ollama

DEFAULT_MODEL = "gemma4:e4b-mlx"

# --- contract bounds (kept in sync with enrich-validate) ---------------------
DESC_MAX = 160
TAGS_MIN = 3
TAGS_MAX = 12
# A tag is 1-2 short lowercase tokens (allow an internal hyphen/space), no other
# punctuation. We normalize toward this; the validator enforces it.
_TAG_OK = re.compile(r"^[a-z0-9]+(?:[ -][a-z0-9]+)?$")
_TAG_STRIP = re.compile(r"[^a-z0-9 -]")
# Filler tags that add no search value — dropped from LLM-generated tags only
# (native vendor tags are always preserved verbatim).
_GENERIC_TAGS = frozenset(
    {
        "icon", "symbol", "object", "ui", "vector", "image", "graphic", "sign",
        "shape", "standard", "general", "item", "element", "interface", "logo",
        "design", "graphical", "pictogram", "glyph",
    }
)

# --- frozen prompt -----------------------------------------------------------
_PROMPT_BASE = """You are labeling a single user-interface icon for a searchable icon library.
The image is one icon, rendered black-on-white. It is a symbol, not a photo.

Identify the concrete shapes you actually see, then name the common real-world
concept they represent (e.g. a mortarboard = graduation/education; two arrows
merging = merge).

Read small modifier marks layered on a base symbol — they change the meaning, so
name them: a diagonal slash through a symbol = disabled, off, muted, or not
allowed; an X = remove, close, or error; a plus = add or new; a minus = remove;
a checkmark = done or confirmed; a small arrow = direction or movement; an
enclosing circle or square = a status or action wrapper. If the icon is a
stylized brand mark you do not recognize, describe its geometry, never guess the
company.

Output RAW JSON only — no markdown, no code fences (```), no preamble such as
"Here is". Reply with the JSON object and nothing else. If you cannot make out
the image, still return your best-guess JSON; never answer in prose.

Rules:
- "description": ONE factual sentence, at most 160 characters, no markdown.
  Name the literal shape AND its common meaning. Be specific enough that a
  near-duplicate icon (e.g. an arrow vs an arrow-in-a-circle vs a chevron)
  would get a DIFFERENT description. Do not invent brand names or guess a
  company. Do not start with "An icon of"; describe the thing itself.
{tags_rule}"""

_TAGS_RULE = """- "tags": {min}-{max} lowercase keywords a user might search for. Single words
  or very short tokens, no punctuation, no duplicates, no sentences.""".format(
    min=TAGS_MIN, max=TAGS_MAX
)

_NO_TAGS_RULE = '- Do not output tags; only the description.'

_NAME_HINT = (
    '\n\nThe library\'s filename for this icon is "{name}". Use it only as a weak '
    "hint; trust the image over the name, and never copy the raw filename into the "
    "description."
)

_TAGS_HINT = (
    "\n\nKnown keywords for this icon: {tags}. Use them to disambiguate the "
    "concept (e.g. a letter with arrows often means font-size), but still "
    "describe the actual shapes you see."
)

# Descriptions where the model claimed it had no image / refused — never store.
_REFUSAL = re.compile(
    r"\b(no image|image not provided|not provided|cannot (see|view|identify)|"
    r"unable to (see|view)|provide (the|an) (image|icon)|need an image|"
    r"i (can'?t|cannot) see)\b",
    re.I,
)


class LLMError(RuntimeError):
    """Raised when the model could not produce a valid record after retries."""


def _schema(need_tags: bool) -> dict:
    props = {
        "description": {
            "type": "string",
            "description": f"One factual sentence, <= {DESC_MAX} chars.",
        }
    }
    required = ["description"]
    if need_tags:
        props["tags"] = {
            "type": "array",
            "items": {"type": "string"},
            "description": f"{TAGS_MIN}-{TAGS_MAX} lowercase search keywords.",
        }
        required.append("tags")
    return {"type": "object", "properties": props, "required": required}


def _build_prompt(
    name: str | None, need_tags: bool, hint_tags: list[str] | None = None
) -> str:
    prompt = _PROMPT_BASE.format(
        tags_rule=_TAGS_RULE if need_tags else _NO_TAGS_RULE
    )
    if name:
        prompt += _NAME_HINT.format(name=name)
    if hint_tags:
        prompt += _TAGS_HINT.format(tags=", ".join(hint_tags))
    return prompt


def normalize_tags(raw: list) -> list[str]:
    """Lowercase, strip punctuation, dedupe (order-preserving), drop empties."""
    out: list[str] = []
    seen: set[str] = set()
    for t in raw or []:
        if not isinstance(t, str):
            continue
        tag = _TAG_STRIP.sub("", t.strip().lower()).strip(" -")
        tag = re.sub(r"\s+", " ", tag)
        if tag and tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out


_FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def extract_json(content: str) -> dict | None:
    """
    Parse a JSON object from model output. Not every vision model honors
    ollama's ``format=<schema>`` (the default MLX runner does not), so output
    may be markdown-fenced or have prose around it. Try, in order: raw parse,
    fenced block, first balanced ``{...}`` span.
    """
    if not content:
        return None
    for candidate in (content, *(m.group(1) for m in _FENCE.finditer(content))):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    start = content.find("{")
    end = content.rfind("}")
    if 0 <= start < end:
        try:
            obj = json.loads(content[start : end + 1])
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return None


def normalize_description(raw) -> str:
    if not isinstance(raw, str):
        return ""
    desc = " ".join(raw.split()).strip()
    # Strip a stray leading "An icon of"/"Icon of" if the model ignored the rule.
    desc = re.sub(r"^(an?\s+)?icon (of|depicting|showing)\s+", "", desc, flags=re.I)
    if not desc:
        return ""
    desc = (desc[0].upper() + desc[1:])[:DESC_MAX].strip()
    # Ensure a single terminal period for consistency across vendors.
    if desc and desc[-1] not in ".!?":
        desc = (desc[: DESC_MAX - 1].rstrip() + ".") if len(desc) >= DESC_MAX else desc + "."
    return desc


def generate(
    png_path: Path,
    name: str | None,
    vendor: str,
    need_tags: bool,
    model: str = DEFAULT_MODEL,
    use_name_hint: bool = True,
    hint_tags: list[str] | None = None,
    retries: int = 2,
) -> dict:
    """
    Run the vision model on ``png_path`` and return
    ``{"description": str, "tags": [str]}`` (``tags`` empty when not requested).

    ``hint_tags`` (e.g. native vendor tags) ground the description for ambiguous
    glyphs. Retries on malformed/empty/refusal output up to ``retries`` times.
    """
    prompt = _build_prompt(name if use_name_hint else None, need_tags, hint_tags)
    schema = _schema(need_tags)
    last_err = ""
    for attempt in range(retries + 1):
        # temperature=0 for the deterministic first pass; bump on retry so a
        # deterministic refusal/garble can actually recover.
        temperature = 0 if attempt == 0 else 0.4
        try:
            resp = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt, "images": [str(png_path)]}],
                format=schema,
                options={"temperature": temperature},
            )
        except Exception as e:  # network / model errors
            last_err = f"ollama.chat failed: {e}"
            continue
        content = (resp.get("message") or {}).get("content", "")
        data = extract_json(content)
        if data is None:
            last_err = f"non-JSON content: {content[:120]!r}"
            continue
        desc = normalize_description(data.get("description"))
        tags = normalize_tags(data.get("tags", [])) if need_tags else []
        # Drop filler tags (LLM path only); keep at least the strongest few.
        if need_tags:
            filtered = [t for t in tags if t not in _GENERIC_TAGS]
            tags = filtered if len(filtered) >= TAGS_MIN else tags
        if not desc:
            last_err = "empty description"
            continue
        if _REFUSAL.search(desc):
            last_err = f"refusal/no-image description: {desc!r}"
            continue
        if need_tags and len(tags) < TAGS_MIN:
            last_err = f"too few tags: {tags}"
            continue
        if need_tags and len(tags) > TAGS_MAX:
            tags = tags[:TAGS_MAX]
        return {"description": desc, "tags": tags}
    raise LLMError(f"{vendor}/{name}: {last_err}")
