# 한국 기업 로고 모음 (`kr-logos`)

> 한국 기업의 로고·심볼·워드마크를 **AI 에이전트가 직접 조사·수집·검증**하여
> 큐레이션하는, 출처(provenance)가 보증된 브랜드 자산 카탈로그.

[Grida Icons](../README.md)의 하위 세트(set)입니다. id는 `kr-logos`,
빌드 산출물은 [`dist/kr-logos/`](../dist)에 생성되어 다른 세트와 동일한 검색
API·웹앱으로 서빙됩니다. (브랜드 자산이므로 분류상 `logos`로 집계됩니다.)

---

## 왜 이 세트는 다른가 (Why this set is different)

이 레포의 다른 모든 세트(`svgl`, `heroicons`, `lucide-icons` …)는 **신뢰할 수
있는 상위 저장소(upstream)를 git submodule로 미러링**합니다. 누군가 이미
큐레이션·정규화·유지보수한 데이터를 그대로 가져오는 구조입니다.

**`kr-logos`에는 그런 upstream이 없습니다.**

한국 기업은 대체로

- 브랜드 사이트나 프레스킷(press kit)이 **아예 없거나**,
- 있어도 **저해상도 PNG·JPG뿐이거나 구버전 로고**이고,
- 제3자 로고 사이트의 자료는 **출처 불명·왜곡·오래됨**이라 믿을 수 없습니다.

그래서 이 세트에서는 **에이전트(AI)가 곧 파이프라인**입니다.
직접 **조사(research) → 브라우저로 다운로드(download) → 검증(verify)** 한 결과만
레포에 커밋합니다. submodule 미러가 아니라, 큐레이션된 자산을 레포에 직접 보관합니다.

그래서 이 프로젝트의 가치는 "로고 파일" 그 자체가 아니라,
**모든 자산에 붙은 출처·증거·검증 기록(provenance & evidence)** 에 있습니다. 우리는
로고가 정답이라고 단정하지 않고, **정답인지 판단할 근거를 규격화된 포맷으로 저장**
합니다 — 신뢰할 수 없는 세상에서 신뢰할 수 있는 카탈로그를 만드는 유일한 길입니다.

---

## 독트린 (Doctrine)

이 세트에 자산을 추가·수정하는 모든 작업(사람이든 에이전트든)은 아래 8개 원칙을 따릅니다.

### 1. 출처 없는 자산은 자산이 아니다 (Provenance-first)

모든 SVG는 **출처 기록(provenance record)** 과 1:1로 묶입니다. 어디서, 언제,
어떻게 가져왔고, 누가 어떻게 검증했는지 없이는 **커밋하지 않습니다.** 출처를
기록할 수 없는 파일은 품질이 아무리 좋아도 받지 않습니다.

### 2. 출처에는 등급이 있다 (Source tiers)

모든 출처는 신뢰도에 따라 **T0 ~ T4 등급**을 가지며, 항상 **가장 낮은 번호(=가장
신뢰도 높은) 등급을 우선**합니다. 더 좋은 출처를 찾으면 기존 자산을 교체합니다.
([출처 등급](#출처-등급-source-tiers) 참고)

### 3. 검증 없이는 커밋 없다 (Verify before commit)

다운로드한 그대로 믿지 않습니다. **공식 렌더링과 시각 대조**, **브랜드 컬러(hex)
대조**, **비율·치수 확인**, **현행 로고인지(리브랜딩 여부) 확인**을 통과해야
합니다. 검증 방법과 신뢰도(confidence)를 기록에 남깁니다.
([검증 체크리스트](#검증-체크리스트-verification-checklist) 참고)

### 4. 벡터 우선, 충실도 우선 (Vector-first, fidelity-first)

가능한 한 **원본 벡터(SVG/PDF/AI/EPS)** 를 확보합니다. 래스터(PNG/JPG)밖에 없을
때만 벡터화하며, 이때는 반드시 `T4 / low confidence`로 표기합니다. 임의로 "보기
좋게" 다시 그리지 않습니다 — 우리는 **원본을 보존**하지 디자인하지 않습니다.

### 5. 상표는 자산이 아니라 참조다 (Trademarks, not assets)

여기 수록된 로고는 각 기업의 **등록 상표·저작물**입니다. 수록은 사용 권리를
부여하지 않습니다. 이 카탈로그는 **식별·참조(reference) 목적**이며, 사용 전
권리자의 상표 사용 지침을 확인해야 합니다. ([법적 고지](#법적-고지-legal-notice) 참고)

### 6. 한국 기업의 정체성을 정확히 모델링한다 (Korean corporate identity)

이름이 곧 식별자입니다. 한글명/영문명/법인명/그룹(계열) 관계/종목코드/DART 고유번호를
정확히 기록해, 동음이의·계열사 혼동·구사명을 방지하고 **공적 기록으로 교차검증**이
가능하게 합니다. ([네이밍과 식별](#네이밍과-식별-naming--identity) 참고)

### 7. 누구나 재검증할 수 있어야 한다 (Auditable & reproducible)

출처 URL·캡처 일시·방법을 남겨 **제3자가 동일 경로로 재확인**할 수 있게 합니다.
출처 링크가 죽으면(link rot) 캡처 일시와 방법으로 추적 가능해야 하며, 가능하면
아카이브(웹 아카이브 등) 링크를 함께 남깁니다.

### 8. 정답이 아니라 근거를 저장한다 (Evidence over answers)

대부분의 경우 "이 로고가 진짜 현행 정답인지" 단정하기 어렵습니다. 그래서 우리는
**정답을 주장하지 않고, 정답 여부를 판단할 근거(evidence)를 규격화된 포맷으로
저장**합니다. 자산마다 다음을 남깁니다.

1. **증거(evidence)** — 이 로고가 맞다는 근거 링크(공식 현행 맥락에서의 사용 등).
2. **리브랜드 연혁(history)** — 마지막 리브랜드 일자. 이력이 없으면 최초/설립 일자.
   규모 있는 기업은 뉴스에 로고 변경이 언급되니 **뉴스 검색으로 일자를 못 박는다.**
3. **관련 소스 링크 전부(related_sources)** — 조사 중 본 모든 근거 URL.
4. **계열사·동음이의 배제 근거** — 같은 그룹의 다른 계열사 로고가 아님을 확인.

불확실하면 불확실하다고 기록하고(`confidence`/`open_questions`) `needs-review`로
둡니다. **모르는 것을 안다고 쓰지 않습니다.**

---

## 수록 범위 (Scope)

**수록 대상**

- KRX(KOSPI·KOSDAQ) 상장 기업
- 대기업집단(재벌) **그룹 및 주요 계열사**
- 비상장이지만 사회적으로 널리 알려진 기업
- 주요 스타트업·유니콘, 대표 브랜드/서비스

**범위 밖 (별도 논의)**

- 한국 기업이 아닌 곳
- 정부·공공기관·지자체 (필요 시 별도 세트)
- 폐업·합병으로 사라진 기업의 로고 — 역사적 가치가 있으면 `deprecated` 상태로만 보존

판단이 애매하면 PR에서 논의합니다. "한국 기업인가"의 1차 기준은 **본사 소재지와
법인 등록(국내 법인)** 입니다.

---

## 출처 등급 (Source tiers)

낮은 번호일수록 신뢰도가 높습니다. **항상 확보 가능한 가장 낮은 등급을 선택**하세요.

| 등급   | 이름                       | 정의                                                                                          | 신뢰도 |
| ------ | -------------------------- | --------------------------------------------------------------------------------------------- | ------ |
| **T0** | 공식 브랜드 자산           | 기업이 직접 배포하는 브랜드 가이드라인·프레스킷·다운로드센터의 **벡터 파일**                   | 최상   |
| **T1** | 공식 채널 추출             | 공식 웹사이트·IR 사이트·모바일 앱에 **인라인된 SVG**, 또는 공식 PDF(IR·사업보고서)에서 벡터 추출 | 상     |
| **T2** | 공적·규제 기록             | DART 전자공시, 특허청 KIPRIS 상표 도형, 거래소 자료 등 **공신력 있는 공적 출처**               | 중상   |
| **T3** | 평판 있는 제3자            | 위키미디어 공용, SVGL, Brandfetch, seeklogo 등 — **출처가 명시되고 교차검증 가능한 경우만**     | 중     |
| **T4** | 재구성 (Reconstruction)    | 래스터 벡터화 또는 수작업 재현. **원본 부재 시 최후 수단**, 반드시 공식과 시각 대조            | 하     |

규칙:

- **T4 자산은 `confidence: low` + `status: needs-review`** 로만 커밋할 수 있습니다.
- T3은 출처 URL과 **교차 출처(두 번째 근거)** 가 있어야 합니다.
- 더 낮은 등급의 출처를 새로 찾으면 **즉시 교체**하고 provenance를 갱신합니다.

---

## 수집 워크플로우 (Workflow: 조사 → 다운로드 → 검증)

에이전트가 로고 하나를 추가하는 표준 절차입니다.

### 1단계 — 조사 (Research)

- 기업의 **정규 정체성** 확정: 한글명·영문명·법인명·그룹/계열·**종목코드**·**DART
  고유번호**. (`WebSearch`, DART, 거래소, 위키 활용)
- **계열사·동음이의 배제** — 검색 결과에 같은 그룹의 **다른 계열사 로고**나 동명
  해외기업이 섞일 수 있다. `stock_code`/`dart_corp_code`로 엔티티를 못 박고 잘못된
  후보를 배제한다. (예: '삼성' 검색 시 삼성SDS·삼성물산 로고 혼입 주의)
- **뉴스·연혁 조사 (리브랜드 타임라인)** — 규모 있는 곳은 리브랜딩을 했거나 뉴스에서
  로고가 언급된다. **마지막 리브랜드 일자**를 찾아 현행성을 검증한다. 리브랜드
  이력이 없으면 **최초/설립 일자**를 기준으로 한다. 찾은 **관련 소스 링크를 모두**
  기록한다(`history.sources`, `related_sources`).
- **이 로고가 맞다는 증거 확보** — 공식 현행 맥락(홈페이지 헤더·뉴스룸·브랜드 가이드
  등)에서 동일 로고가 쓰이는 것을 1개 이상 확보해 `evidence`에 남긴다.
- **존속 여부(liveness) 확인** — 폐업·파산·합병으로 사라진 기업인지 확인한다. 공식
  사이트가 죽었거나(HTTP 000/도메인 만료) 회생·파산 뉴스가 있으면 현행성·진위 판정이
  무효이므로 `deferred`(또는 `deprecated`)로 두고 사유를 기록한다. (예: 발란 — 2026 파산)
- 후보 출처를 등급순으로 탐색: T0(브랜드 가이드) → T1(공식 사이트/앱/IR PDF) → …

### 2단계 — 다운로드 (Download)

- **브라우저로 직접** 가져옵니다. (Claude in Chrome MCP 우선, 필요 시 computer-use)
- 우선순위: ① 공식 벡터 다운로드 → ② 페이지 **인라인 SVG 추출** → ③ 공식 PDF에서
  벡터 추출 → ④ (최후) 래스터 → 벡터화.
- **출처 URL과 캡처 일시**를 즉시 기록. 가능하면 아카이브 링크도 확보.

#### 로고 자산 탐색 체크리스트 (Discovery checklist — 이 순서로 전부 확인)

> ⚠️ **홈페이지 헤더만 보고 "벡터 없음/래스터뿐"으로 단정 금지.** 한국 기업은
> 헤더에 PNG를 깔아도 **별도 CI/브랜드 페이지에 공식 벡터(AI/EPS/SVG)** 를 두는
> 경우가 많다. 아래를 **전부** 확인한 뒤에만 needs-review로 강등한다.

1. **공식 CI/BI·브랜드 페이지 (T0, 최우선)** — 사이트에서 다음을 찾는다:
   - 푸터/소개 메뉴의 `CI`·`BI`·`브랜드`·`Brand`·`Identity`·`다운로드센터` 링크.
   - 흔한 URL 패턴 직접 시도: `/ci`, `/bi`, `/brand`, `/company/CI(.aspx)`,
     `/about/ci`, `/kr/company/ci`, `/ir`(투자정보 내 CI), `/pr/ci`.
   - 거기서 **AI·EPS·SVG·PDF·ZIP** 다운로드 링크를 수집한다(예: `Logotype_AI.zip`).
2. **홈페이지/앱 인라인 SVG·img·CSS background** (T1).
3. **공식 PDF(IR·사업보고서·브랜드 가이드)** 에서 벡터 추출 (T1~T2).
4. **AI/EPS 변환** — `.ai`는 PDF 호환이면 `pdftocairo -svg file.ai out.svg` 로
   실벡터가 나온다(특히 구버전 AI). **반드시 변환을 시도해보고** path 수·`<image>`
   유무로 실벡터/래스터를 판정한다. (신형 AI는 래스터 프리뷰만일 수 있음 → 그때만 포기)
   - 브랜드 가이드 시트(여러 변형이 한 페이지)에서 로고만 분리: **색상(brand hex)·
     위치(좌표)로 필터링** 후 `viewBox`를 콘텐츠 bbox로 크롭.
5. **제3자(T3)** — 위키미디어 공용(진짜 SVG), SVGL, Brandfetch. (주의: 나무위키의
   `i.namu.wiki/*.svg`는 **실제로 WebP 래스터를 서빙** — 진짜 벡터 아님.)
6. 위 1~5가 모두 실패할 때만 **래스터 → needs-review(벡터 없음)** 또는 T4 재구성.

> 실패 보고 의무: 어디까지 확인했는지(특히 **CI 페이지 존재/부재**)를 `notes`에
> 남긴다. "래스터뿐"은 CI 페이지를 확인한 뒤에만 쓸 수 있는 결론이다.

### 3단계 — 정규화 (Normalize)

- SVG 정리: 불필요한 메타데이터·주석·하드코딩 width/height 제거, `viewBox` 정상화,
  좌표/색상 보존. (다른 세트와 동일하게 `src/`를 공통 부모로 두는 레이아웃)
- 변형(variant) 도출: `theme`(light/dark), `kind`(symbol/wordmark/lockup).
- 색상은 **원본 brand hex 보존**. 단색(mono) 변형이 공식 자산일 때만 별도 추가.

### 4단계 — 검증 (Verify)

- [검증 체크리스트](#검증-체크리스트-verification-checklist)를 통과해야 합니다.
- 통과 시 `verified: true`, 검증자·방법·`confidence` 기록.

### 5단계 — 출처 기록 (Record provenance)

- [provenance 스키마](#1-소스-source-of-truthkr-logos)의 모든 필드를 채웁니다.

### 6단계 — 커밋 & 리뷰 (Commit & review)

- **검증을 통과한 자산만** 커밋. `main`에서 분기해 PR을 올리고 **사람이 diff를
  리뷰**한 뒤 머지합니다. (자동 업데이트 대상이 아님 — [데이터 갱신](#데이터-갱신) 참고)

---

## 검증 체크리스트 (Verification checklist)

자산 하나를 `verified: true`로 표시하기 전 모두 통과해야 합니다.

- [ ] **정체성 일치** — 이 로고가 기록된 기업·계열사의 것이 맞는가 (동음이의/계열사 혼동 없음)
- [ ] **현행성** — 최신 로고인가 (리브랜딩으로 폐기된 버전이 아닌가)
- [ ] **시각 대조** — 공식 렌더링과 나란히 비교해 형태·자간·비율이 일치하는가
- [ ] **컬러 정확도** — 브랜드 가이드의 hex와 일치하는가 (근사치면 기록에 명시)
- [ ] **벡터 무결성** — 깨진 path·잘림·래스터 임베드·폰트 미아웃라인 없는가
- [ ] **테마/변형** — light/dark, symbol/wordmark/lockup 분류가 정확한가
- [ ] **출처 신뢰** — 등급(T0~T4)과 confidence가 출처 실체와 부합하는가
- [ ] **재현 가능** — 기록된 출처 URL·방법으로 제3자가 같은 결과에 도달할 수 있는가
- [ ] **증거 확보** — 이 로고가 맞다는 증거(공식 현행 맥락)를 1개 이상 `evidence`에 기록했는가
- [ ] **리브랜드 타임라인** — 마지막 리브랜드(또는 최초/설립) 일자 + 출처를 `history`에 기록했는가
- [ ] **계열사 배제** — 동일 그룹의 다른 계열사·동명 기업 로고가 아님을 근거와 함께 확인했는가
- [ ] **불확실성 명시** — 못 정한 부분은 `open_questions`에 적고 `confidence`를 정직하게 표기했는가

---

## 데이터 스키마 (Data schema)

두 개의 레이어로 나뉩니다. **소스(source of truth)** 는 풍부한 출처·검증 정보를
담고, **빌드 산출물(dist)** 은 다른 세트와 동일한 계약(contract)으로 정규화됩니다.

### 1. 소스 (source of truth, `kr-logos/`)

기업 단위로 묶고, 각 기업 디렉터리에 SVG들과 `company.json`(정체성 + 자산별
provenance)을 둡니다.

```
kr-logos/
  README.md                       # 본 독트린 (this file)
  companies/
    samsung-electronics/
      company.json                # 정체성 + 자산 목록 + provenance
      samsung-electronics-symbol-light.svg
      samsung-electronics-symbol-dark.svg
      samsung-electronics-wordmark-light.svg
    ...
```

`company.json` 예시:

```jsonc
{
  "id": "samsung-electronics",
  "identity": {
    "name_ko": "삼성전자",
    "name_en": "Samsung Electronics",
    "legal_name_ko": "삼성전자 주식회사",
    "legal_name_en": "Samsung Electronics Co., Ltd.",
    "aliases": ["삼성", "Samsung", "SEC"],
    "group_ko": "삼성그룹",
    "group_en": "Samsung Group",
    "stock_code": "005930",        // KRX 종목코드
    "dart_corp_code": "00126380",  // DART 고유번호 (공적 교차검증 키)
    "homepage": "https://www.samsung.com",
    "industry": "전자/반도체",
    "affiliate_note": "삼성그룹 계열 — 종목코드 005930(삼성전자) 한정. 삼성SDS·삼성물산 등 계열사 로고와 구분"
  },
  "history": {
    "founded": "1969-01-13",
    "last_rebrand": "2015",          // 마지막 리브랜드 일자 (YYYY 또는 YYYY-MM-DD)
    "is_original": false,            // 리브랜드 이력 없는 최초 로고면 true
    "basis": "rebrand-news",         // rebrand-news | founding-date | unknown
    "sources": [
      "https://...(2015 로고 변경 보도)",
      "https://...(공식 연혁 페이지)"
    ]
  },
  "related_sources": [               // 조사 중 본 모든 근거 링크
    "https://en.wikipedia.org/wiki/Samsung_Electronics",
    "https://namu.wiki/w/삼성전자"
  ],
  "assets": [
    {
      "file": "samsung-electronics-symbol-light.svg",
      "properties": { "theme": "light", "kind": "symbol" },
      "provenance": {
        "source_tier": "T0",
        "source_name": "삼성전자 브랜드 가이드라인",
        "source_url": "https://...",
        "archive_url": "https://web.archive.org/...",   // 선택
        "original_format": "svg",
        "captured_at": "2026-06-14",
        "capture_method": "browser:inline-svg-extract", // download | inline-svg-extract | pdf-extract | vectorized-from-raster | manual-reconstruction
        "captured_by": "agent:claude-code"
      },
      "evidence": [                  // 이 로고가 "맞다"는 근거 (정답이 아니라 판단 근거)
        { "type": "official-current-context", "url": "https://www.samsung.com", "note": "공식 홈페이지 헤더에 동일 워드마크 사용 (확인 2026-06-14)" },
        { "type": "press-release", "url": "https://news.samsung.com/...", "note": "공식 뉴스룸에서 동일 로고 사용" }
        // type: official-current-context | brand-guideline | press-release | trademark-record | news-article | screenshot
      ],
      "verification": {
        "verified": true,
        "verified_at": "2026-06-14",
        "verified_by": "agent:claude-code",
        "method": ["visual-diff-vs-official", "brand-hex-check", "rebrand-timeline-check"],
        "confidence": "high",       // high | medium | low
        "open_questions": []        // 미해결 의문점 — 있으면 needs-review 권장
      },
      "status": "published",        // draft | needs-review | verified | published | deprecated
      "trademark_owner": "삼성전자 주식회사",
      "notes": ""
    }
  ]
}
```

### 2. 빌드 산출물 (`dist/kr-logos/data.json`)

파이프라인이 소스를 빌드해 **다른 세트와 동일한 형태**로 만듭니다. 검색 API·웹앱은
이 파일만 읽습니다.

```jsonc
{
  "name": "Korean Company Logos",
  "vendor": "kr-logos",
  "categories": ["grida://library/categories/logos"],
  "version": "0.1.0",
  "description": "AI-curated, provenance-verified logos of Korean companies.",
  "license": "see LICENSE / per-mark trademark owners",
  "variants": {
    "theme": { "title": "Theme", "default": "light", "enum": ["light", "dark"] },
    "kind":  { "title": "Variant", "default": "symbol", "enum": ["symbol", "wordmark", "lockup"] }
  },
  "files": [
    {
      "name": "samsung-electronics-symbol-light",
      "file": "src/samsung-electronics-symbol-light.svg",
      "properties": { "theme": "light", "kind": "symbol" },
      "description": "...",   // enrichment 단계에서 채움
      "tags": ["삼성", "samsung", "전자", "electronics", "반도체", ...]
    }
  ]
}
```

> `description`/`tags`는 다른 세트와 같은 enrichment 텍스트 레이어입니다. 검증된
> 정체성(한글명·영문명·별칭·그룹·업종)을 태그로 채워 **한/영 양쪽 검색**이
> 되도록 합니다.

---

## 네이밍과 식별 (Naming & identity)

- **company id** — 영문 kebab-case, 안정적 식별자. 보통 `name_en` 기반
  (`samsung-electronics`, `hyundai-motor`, `naver`, `kakao`).
- **계열사 구분** — 그룹과 계열사를 별개 엔트리로 두고 `group_*`으로 연결합니다.
  (예: `samsung-electronics`, `samsung-sds`, `samsung-biologics` → 모두 `삼성그룹`)
- **교차검증 키** — `stock_code`(상장사)와 `dart_corp_code`는 동음이의·계열사
  혼동을 막는 공적 식별자입니다. 가능하면 반드시 채웁니다.
- **파일명** — `<company-id>[-<kind>][-<theme>].svg`.
  예: `kakao-symbol-light.svg`, `naver-wordmark-dark.svg`.

---

## 변형 축 (Variant axes)

다른 로고 세트(`svgl`)와 호환되는 축을 사용합니다.

- `theme` — `light` | `dark` (밝은/어두운 배경용)
- `kind` — `symbol`(심볼/마크) | `wordmark`(로고타입/글자) | `lockup`(심볼+워드마크 결합)

색상 단색화(mono) 등 추가 축은 **공식 자산으로 존재할 때만** 도입합니다.

---

## 상태 수명주기 (Status lifecycle)

```
draft → needs-review → verified → published
                                      └→ deprecated  (리브랜딩/폐업으로 폐기)
```

- `published`만 검색·API에 노출됩니다.
- 더 좋은 출처로 교체 시 provenance를 갱신하고 등급/confidence를 재평가합니다.

---

## 파이프라인 통합 (Pipeline integration)

- 빌더 `pipeline/vendor_kr_logos.py`(예정)가 `kr-logos/companies/**`를 읽어
  `dist/kr-logos/{data.json, src/*.svg, LICENSE}`를 생성합니다.
- 빌드는 분류상 **`logos`** 로 집계되어 [`dist/stats.json`](../dist/stats.json)의
  `totals.logos`와 루트 README의 logos 뱃지에 반영됩니다.
- 이후 다른 세트와 동일하게 **enrichment(설명/태그)** → 검색 인덱스 → API
  (`/api`, `/api/logos`, `/dist/kr-logos/...`) 로 흐릅니다.
- `validate` 게이트: 각 `company.json` 파싱, 자산 파일 존재, **모든 `published`
  자산이 `verified: true`** 임을 검사합니다.

> 상세 파이프라인 규약은 [`pipeline/README.md`](../pipeline/README.md) 참고.

## 데이터 갱신

이 세트는 **submodule이 아니므로 주간 자동 업데이트 대상이 아닙니다.**
([루트 update-icons 워크플로우](../README.md#keeping-data-fresh)는 vendor
submodule만 갱신). `kr-logos`는 **사람/에이전트의 큐레이션 PR**로만 갱신되며,
리브랜딩 모니터링과 출처 등급 상향(T3→T0 등)은 수시로 진행합니다.

---

## 법적 고지 (Legal notice)

- 수록된 로고·심볼·워드마크는 각 기업의 **등록 상표 및 저작물**이며, 권리는 전적으로
  해당 기업(권리자)에 귀속됩니다.
- **수록은 사용 라이선스를 의미하지 않습니다.** 본 카탈로그는 식별·참조(reference)
  목적이며, 사용 전 각 권리자의 **상표 사용 지침**을 확인해야 합니다.
- 제3자 출처(T3)에서 가져온 자산은 해당 출처의 라이선스/이용약관도 함께 확인합니다.
- 권리자가 삭제(takedown)를 요청하면 **신속히 수용**합니다. 이의는 PR/이슈로 접수합니다.
- 이 문서는 법률 자문이 아닙니다.

---

## 기여 / 에이전트 가이드 (Contributing)

1. `main`에서 분기. 기업 단위로 `companies/<id>/` 디렉터리를 만들고
   `company.json` + SVG를 추가합니다.
2. [수집 워크플로우](#수집-워크플로우-조사--다운로드--검증)와
   [검증 체크리스트](#검증-체크리스트-verification-checklist)를 그대로 따릅니다.
3. **출처·증거·검증 기록이 없으면 PR을 올리지 않습니다** — 정답을 단정하지 말고
   근거(`evidence`·`history`·`related_sources`)를 규격대로 채웁니다. (독트린 1·3·8)
4. 포맷/린트는 루트 `oxfmt`/`oxlint`에 맡깁니다. 생성 산출물(`dist/`)은 빌드로 만듭니다.
5. 레포 전반의 에이전트 규약은 [`../AGENTS.md`](../AGENTS.md) 참고.

---

## 라이선스 (License)

빌드 산출물 라이선스 처리는 [`../LICENSE`](../LICENSE) 및 `dist/kr-logos/LICENSE`를
따릅니다. **개별 마크의 권리는 각 기업에 귀속**되며, 본 컬렉션의 큐레이션·메타데이터
구조에 대한 라이선스와 상표 자체의 권리는 별개입니다. ([법적 고지](#법적-고지-legal-notice) 참고)
