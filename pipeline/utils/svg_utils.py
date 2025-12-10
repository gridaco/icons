import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, Any


def parse_svg_basic(path: Path) -> Dict[str, Any]:
    """
    Parse basic SVG attributes: viewBox, width, height.
    Falls back to viewBox values when width/height are not present or not numeric.
    """
    result: Dict[str, Any] = {
        "viewBox": None,
        "width": None,
        "height": None,
    }
    if not path.exists():
        return result

    try:
        tree = ET.parse(path)
        root = tree.getroot()
        view_box = root.attrib.get("viewBox")
        width = root.attrib.get("width")
        height = root.attrib.get("height")

        result["viewBox"] = view_box

        def _as_number(value: Optional[str]) -> Optional[float]:
            if value is None:
                return None
            try:
                return float(value)
            except ValueError:
                return None

        width_num = _as_number(width)
        height_num = _as_number(height)

        if width_num is None and view_box:
            parts = view_box.split()
            if len(parts) == 4:
                width_num = float(parts[2])
        if height_num is None and view_box:
            parts = view_box.split()
            if len(parts) == 4:
                height_num = float(parts[3])

        result["width"] = width_num
        result["height"] = height_num
    except Exception:
        # If parsing fails, return whatever was collected (mostly None)
        return result

    return result

