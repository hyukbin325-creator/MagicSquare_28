# MagicSquare_XX

4×4 마방진(1~16)을 다루는 학습·실습 프로젝트입니다.  
**불변식 판정·재현 가능한 절차·명시적 계약**을 ECB 아키텍처와 **TDD(Dual-Track)** 로 구현합니다.

---

## 프로젝트 상태

| 항목 | 상태 |
|------|------|
| 문제 정의 (STEP 1~5) | 완료 — [Report/01](Report/01.Problem-Definition-Report.md) |
| PRD·테스트 계획 | [docs/test_plan.md](docs/test_plan.md) (AC-FR-01-01 중심) |
| ECB 스켈레톤 (`src/`) | Boundary·Control 스텁, Entity `user` 샘플 |
| TDD RED (전체) | Boundary 36건 + Entity 12건 + Report/08 AC-FR-01-01 25건 |
| TDD GREEN (진행 중) | **AC-FR-01-01 `grid=None`** — `validate_grid` 분기만 통과 (6건) |
| GUI (`boundary/screen/`) | 미구현 |

**최근 pytest (Boundary + `test_user`):** 16 passed · 25 failed · Entity Track B 4파일 collection ERROR (`src.entity.services` 미생성)

---

## 한 줄 요약

> **4×4 격자 배치가 마방진 불변식을 만족하는지 일관되게 판정하고, 필요 시 유효한 완성 배치를 재현 가능한 절차로 다룬다. 성공은 특정 한 해와의 일치가 아니라 불변식 충족으로 정의한다.**

---

## 아키텍처 (ECB)

| 레이어 | 경로 | 역할 |
|--------|------|------|
| **Boundary** | `src/boundary/` | 입력 검증, 실패 DTO 반환 (`ValidationErrorResponse`) |
| **Control** | `src/control/` | `MagicSquareResolver` — 검증 통과 후 Domain 호출 (스텁) |
| **Entity** | `src/entity/` | 도메인 규칙·계산 (서비스 패키지 GREEN 진행 예정) |

**의존 방향:** `boundary → control → entity` (역방향 import 금지)

**Dual-Track 테스트**

| Track | 경로 | Mock |
|-------|------|------|
| A (UI/Boundary) | `tests/boundary/` | Control `resolve` Mock 허용 |
| B (Domain) | `tests/entity/` | Domain Mock **금지** |

규칙·TDD 단계: [.cursorrules](.cursorrules), [.cursor/rules/](.cursor/rules/)

---

## 저장소 구조

```
MagicSquare_XX/
├── README.md
├── .cursorrules
├── requirements-dev.txt          # pytest, pytest-cov, pydantic
├── docs/
│   └── test_plan.md              # AC·시나리오·커버리지 SSOT
├── Report/                       # 단계별 작업 보고서 (01~10)
├── Prompt/                       # 세션 transcript
├── src/
│   ├── boundary/
│   │   ├── constants.py          # GRID_SIZE, INVALID_SIZE, 메시지 SSOT
│   │   ├── schemas.py            # ValidationErrorResponse (pydantic)
│   │   └── input_validator.py    # validate_grid / handle_input
│   ├── control/
│   │   └── magic_square_resolver.py
│   └── entity/
│       └── user.py               # 샘플 (TDD 스캐폴드와 별도)
└── tests/
    ├── boundary/
    │   ├── test_input_validator_ac_fr_01_01.py   # AC-FR-01-01 Full RED
    │   ├── test_u_in.py / test_u_out.py / test_u_flow.py  # Track A 스켈레톤
    │   └── conftest.py
    └── entity/
        ├── test_d_loc_01.py … test_d_sol.py      # Track B 스켈레톤
        └── conftest.py                           # G0~G3 fixture 주석
```

---

## 개발 환경

- **Python:** 3.10+ (로컬 3.13 확인)
- **설치:** `pip install -r requirements-dev.txt`
- **전체 Boundary 테스트:** `python -m pytest tests/boundary/ -v`
- **AC-FR-01-01 None 분기 (GREEN 확인):**

```bash
python -m pytest tests/boundary/test_input_validator_ac_fr_01_01.py::TestAcFr0101NormalFailureReturn::test_none_grid_returns_invalid_size_failure_result -v
```

- **커버리지 (선택):** `pytest --cov=src --cov-report=term-missing`

---

## AC-FR-01-01 계약 (형상 검증 앵커)

| 입력 | 기대 |
|------|------|
| `grid=None` | `code="INVALID_SIZE"`, `message="Grid must be 4x4."` (문자 단위 동일) |
| 형상 위반 (`[]`, 3×4, 4×0열 등) | 동일 코드·메시지, **Domain `resolve()` 0회** |

**현재 구현 (GREEN 범위):** `InputValidator.validate_grid()` — `grid is None` 만 반환.  
`handle_input()`, `[]` / 비정형 크기, U-IN/U-OUT/U-FLOW는 **RED**.

상수 SSOT: `src/boundary/constants.py` (`GRID_SIZE`, `INVALID_SIZE_CODE`, `GRID_SHAPE_ERROR_MESSAGE`)

---

## TDD GREEN 커밋 묶음 (권장 순서)

한 커밋 = **Track 하나** + RED 3~5건(또는 동일 분기 1건). Track A·B 동시 GREEN 금지.

### Track A — Boundary

| 묶음 | 내용 | RED 건수 | 비고 |
|:----:|------|:--------:|------|
| A-0 | `grid=None` · `validate_grid` | 6 | **GREEN 완료** |
| A-0b | fixture 범위 검증 (`ScopeLimitation`) | 5 | **GREEN** (프로덕션 불필요) |
| A-1 | `handle_input(None)` + resolve 격리 | 3 | 다음 권장 |
| A-2 | `grid=[]` | 4 | |
| A-3 | `4행×0열` | 3 | |
| A-4 | `3×4` | 3 | |
| A-5 | `4×3` | 1 | A-4와 합쳐도 됨 |
| A-6 | U-IN-04~07 (E002/E003/E004) | 5 | 스켈레톤 `pytest.fail` |
| A-7 | U-IN-08 + U-FLOW-02 | 3 | |
| A-8 | U-OUT-01~03 | 3 | |

### Track B — Entity

| 묶음 | 내용 | RED 건수 | 비고 |
|:----:|------|:--------:|------|
| B-0 | `src/entity/services/` 패키지 스켈레톤 | — | collection ERROR 해소 선행 |
| B-1 | D-LOC-01 BlankFinder | 1 | |
| B-2 | D-MIS-01 MissingNumberFinder | 1 | |
| B-3 | D-VAL-01~04 합·대각선 | 4 | |
| B-4 | D-VAL-05~06 `is_valid` | 2 | |
| B-5 | D-SOL-01 성공 | 1 | |
| B-6 | D-SOL-03~04 실패 경로 | 2 | |
| B-7 | D-SOL-02 G2 TBD | 1 | 스펙 확정 후 |

**권장 진행:** A-1 → A-2 → … → A-5 → B-0 → B-1~B-7 → A-6~A-8

---

## RED / GREEN 체크리스트 (test_plan 연동)

### Track A — Boundary

- [x] TC-A-01: `grid=None` → 실패 결과 (`validate_grid`)
- [x] TC-A-02: `code == "INVALID_SIZE"`
- [x] TC-A-03: `message == "Grid must be 4x4."`
- [ ] TC-A-04: `grid=None` 시 `resolve()` 0회 (`handle_input` — A-1)
- [ ] TC-A-05: `grid=[]` → 실패 (A-2)
- [ ] TC-A-06: 3×4 / 4×3 / 4×0열 등 형상 불일치 (A-3~A-5)
- [x] TC-A-07: 반환 타입 `ValidationErrorResponse` (`grid=None`)

### Track B — Domain 격리

- [ ] TC-B-01~B-03: Boundary 선행 검증 후 `resolve()` 미호출 (A-1~A-5와 연동)
- [x] TC-B-04: AC-FR-01-02~05는 별도 스코프 (`ScopeLimitation` fixture 테스트)

### 커버리지 목표 (미달)

- [ ] Domain Logic: 95%+
- [ ] Boundary Layer: 85%+
- [ ] 전체: 80%+ (프로젝트 기본선)

### 기타

- [ ] `defect_list.md` 및 결함 추적
- [ ] GUI 수동 확인 (`boundary/screen/` 추가 후)

---

## 배경 · 불변식 · Why

### 표면 vs 실제 문제

- **피할 정의:** “한 장의 마방진을 만드는 프로그램”
- **실제:** 4×4·1~16에 대한 **판정(유효/무효/미완)** + (선택) 완성 절차, **TDD로 계약 고정**

### 핵심 불변식 (마법상수 34)

| ID | 요약 |
|----|------|
| I1~I3 | 값 범위, 완성 시 1~16 각 1회, 부분 상태 무결 |
| I4~I6 | 4행·4열·주·부대각선 합 = 34 |
| I7~I9 | 완성+조건 → 유효; 위반 → 무효; 미완 → 보류 |
| I10~I12 | 검증은 생성 결과를 신뢰하지 않음; 재현·회귀 |

상세: [Report/01 — STEP 5](Report/01.Problem-Definition-Report.md#step-5--진짜-문제-정의)

---

## 확정 / 미확정

| 항목 | 상태 |
|------|------|
| 언어·아키텍처 | Python 3.10+, ECB, pytest |
| 1차 범위 | Boundary 형상(AC-FR-01-01) → Entity 서비스 → U-IN/OUT/FLOW |
| 부분 채움(빈 칸) | PRD·test_plan 기준 허용 (2 blanks 등 후속 AC) |
| 판정 출력 | `{ code, message }` (`ValidationErrorResponse`) |
| GUI | 미착수 |
| `docs/PRD_MagicSquare.md` | 저장소에 없음 — `test_plan.md`·Report/07·08 참고 |

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [Report/01](Report/01.Problem-Definition-Report.md) | 문제 정의 STEP 1~5 |
| [Report/08](Report/08.AC-FR-01-01-TDD-RED-Work-Export-Report.md) | AC-FR-01-01 RED 25건 |
| [Report/10](Report/10.MagicSquare-DualTrack-RED-Skeleton-Work-Export-Report.md) | Dual-Track RED 스켈레톤 23건 |
| [docs/test_plan.md](docs/test_plan.md) | pytest 범위·Mock·커버리지 |

---

## 라이선스 / 기여

미정. 프로젝트 초기 단계입니다.

---

*최종 업데이트: 2026-05-29 — TDD GREEN 진행 (AC-FR-01-01 `grid=None`), ECB·Dual-Track·커밋 묶음 반영*
