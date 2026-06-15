# 회사 리스트 (kr-logos)

수집 대상 한국 기업 목록. 리스트는 **후보(candidate)** 이며, 정답이 아니다 — 각 회사는
[VERIFICATION.md](../VERIFICATION.md) 프레임워크로 개별 검증 후 `companies/`에 기록된다.

## master-500.csv (500개)

구성(혼합형): **상장 인지도 상위 298 + 상장 확장/계열사 122 + 비상장 인지도 80**.

| 컬럼 | 의미 |
|---|---|
| `fame` | 인지도 티어: high / mid / low / private |
| `segment` | `listed`(시총 상위) · `listed-ext`(시총 확장=계열사/중견) · `private`(비상장 큐레이션) |
| `name_ko` | 한글 사명 (KIND/네이버금융 표기) |
| `stock_code` | 종목코드 (비상장은 공란) |
| `market` | KOSPI / KOSDAQ / 비상장 |
| `sector` | 업종 (KIND 표준산업분류) |
| `group` | 대기업집단 추정 태그 (접두사 휴리스틱 — 검증 필요) |
| `homepage` | **공식 홈페이지** (481/500 보유) — 수집 워크플로의 출발점 |
| `ceo` | 대표자명 (KIND) — 무료 신원앵커(B) |
| `listed` | 상장일 |
| `done` | `Y` = 이미 `companies/`에 수집됨 (15개) |
| `note` | 비상장 큐레이션 메모 / 확인필요 플래그 |

## 출처 (sourcing)

1. **KIND 상장법인목록** (한국거래소) — `kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13`
   - 무료, 계정 불필요. EUC-KR HTML 테이블. 상장사 2,762개 전체.
   - 회사명·종목코드·업종·**홈페이지(94%)**·대표자명·상장일·지역 제공. → 상장사 백본의 핵심.
2. **네이버금융 시총순위** — `finance.naver.com/sise/sise_market_sum.naver?sosok=0|1&page=N`
   - 시가총액 = 인지도 프록시(랭킹용). KOSPI(sosok=0)·KOSDAQ(sosok=1), 50개/페이지.
   - 종목코드로 KIND와 결합해 인지도순 정렬.
3. **비상장 80** — 큐레이션(유니콘·핫스타트업·유명 비상장 브랜드). 소스 후보: THE VC(thevc.kr),
   혁신의숲(innoforest.co.kr), 중기부 유니콘 명단, 브랜드평판. 홈페이지는 에이전트 확인값(검증 대상).

### 필터링
- 제거: 우선주(`…우`), 스팩(`…스팩`), 리츠(`…리츠`), **ETF/ETN**(KODEX·TIGER·1Q·액티브 등 발행사 접두사 + 지수/레버리지 키워드).
- `done` 플래그로 기수집 15개 중복 표시(제거하지 않음 — 커버리지 가시화).

### 재현 (regenerate)
KIND xls + 네이버 시총 페이지 → 종목코드 join → 필터 → CSV. (네이버 시총·KIND 표기는 시점에 따라 변동;
종목코드가 키.) 비상장 블록은 수기 큐레이션이라 자동 재현 대상 아님.

## 주의 / TODO
- `group` 태그는 사명 접두사 휴리스틱 → 실제 계열관계와 다를 수 있음(예: '현대'≠전부 현대차그룹). 검증 시 정정.
- 홈페이지 미보유 19개(LG에너지솔루션·카카오뱅크·SK바이오팜 등) → 수집 시 보강.
- `note`에 "확인필요"/"상장일수있음" 표기된 비상장 항목은 상장여부·중복 재확인.
- `name_en`은 미기재 — 수집 단계에서 채움.

## batch-02.csv (40개)
초기 정밀 배치(유명/계열/무명 혼합, 검증 테스트용). master-500과 일부 중복.
