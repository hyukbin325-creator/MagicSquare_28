# MagicSquare_XX

4×4 마방진(1~16)을 다루는 학습·실습 프로젝트입니다.  
현재 단계는 **RED/TDD**이며, “한 장의 표를 만드는 것”보다 **불변식 판정·재현 가능한 절차·명시적 계약**을 다루는 것을 목표로 합니다.

---

## 프로젝트 상태

| 항목 | 상태 |
|------|------|
| 문제 정의 (STEP 1~5) | 완료 |
| 상세 보고서 | [Report/01.Problem-Definition-Report.md](Report/01.Problem-Definition-Report.md) |
| 테스트 계획 | [docs/test_plan.md](docs/test_plan.md) |
| 구현 | RED 진행 중 (Boundary/Control stub, Entity 미구현) |
| 현재 브랜치 | `refactor/refactor` |

---

## 한 줄 요약

> **4×4 격자 배치가 마방진 불변식을 만족하는지 일관되게 판정하고, 필요 시 유효한 완성 배치를 재현 가능한 절차로 다룬다. 성공은 특정 한 해와의 일치가 아니라 불변식 충족으로 정의한다.**

---

## 배경

### 표면에서 보이는 문제 (피해야 할 정의)

“4×4에 1~16을 넣어 합이 같은 마방진 **한 장을 만드는** 프로그램”

→ 특정 격자 모양에 성공이 묶이고, **판정·부분 상태·여러 유효 해**가 빠집니다.

### 실제로 다루는 문제

- **대상:** 4×4 격자, 값 1~16 (완성·부분 배치 모두)
- **1차 목표:** 마방진 **불변식**에 따른 판정 (유효 / 무효 / 미완)
- **2차 목표(선택):** 조건을 만족하는 **완성 배치**를 얻는 절차
- **성공 기준:** 임의의 **유효한** 완성 배치 (교재와 다른 배치도 유효할 수 있음)
- **접근:** 판정 규칙을 먼저 고정하고, **TDD**로 계약·회귀를 통제

---

## 핵심 불변식 (Invariant)

4×4, 1~16 기준 **마법상수 = 34**.

| ID | 요약 |
|----|------|
| **I1~I3** | 값 범위, 완성 시 1~16 각 1회, 부분 상태에서 중복·범위 위반 없음 |
| **I4~I6** | 4행·4열·주대각·부대각선 합 = 34 |
| **I7~I9** | 완성+조건 → 유효; 위반 → 무효; 미완 → 판정 보류 |
| **I10** | 검증은 생성 결과를 신뢰하지 않음 |
| **I11~I12** | 동일 입력 → 동일 판정; 대표 예는 규칙 불변 시 회귀 계약 유지 |

자세한 설명은 [보고서 STEP 5](Report/01.Problem-Definition-Report.md#step-5--진짜-문제-정의)를 참고하세요.

---

## Why 요약

| 단계 | 질문 | 핵심 |
|------|------|------|
| **Why #1** | 왜 완성해야 하는가? | 조건 충족을 **격자 상태로 증명**하기 위함. 유일 정답 vs 유효 해, 완성 vs 검증 구분 필요 |
| **Why #2** | 왜 프로그램인가? | **반복·자동 검증·오류 차단·규칙 명시** — 손계산은 “한 판”, 프로그램은 “절차 고정” |
| **Why #3** | 왜 TDD인가? | **판정권·불변식·입출력 계약**을 먼저 고정. “그림”이 아니라 “실행 가능한 스펙” |

---

## 훈련하려는 사고 능력

- **불변식 사고** — 말로 된 조건을 검사 가능한 목록으로 분해
- **판정권·경계** — 생성 vs 검증 분리, 위반 유형 구분
- **계약·입출력** — Given/Then이 명확한 스펙
- **재현·회귀** — 같은 규칙의 반복 실행과 대표 예
- **문제 재정의** — “마방진 프로그램” → “불변식 + 판정 + (선택) 완성 + 재현”

---

## 문서 구조

```
MagicSquare_XX/
├── README.md                          ← 이 파일 (프로젝트 개요)
├── Report/
│   └── 01.Problem-Definition-Report.md   ← STEP 1~5 전체 보고서
└── Prompting/                         ← 문제 정의 프롬프트 (있는 경우)
```

---

## 문제 정의 단계 (완료)

| STEP | 제목 | 내용 |
|------|------|------|
| 1 | Observation | 상황 관찰, 4×4 맥락 |
| 2 | Why #1 | 완성의 동기와 구조적 모호함 |
| 3 | Why #2 | 프로그램 vs 단순 계산 |
| 4 | Why #3 | TDD, 통제·불변식·입출력 |
| 5 | 진짜 문제 정의 | 표면/개선 정의, Invariant, 사고 능력 |

전체 내용: **[Report/01.Problem-Definition-Report.md](Report/01.Problem-Definition-Report.md)**

---

## 아직 확정되지 않은 사항

구현 전에 결정이 필요한 항목입니다.

- [ ] 1차 범위: **검증만** vs **생성 포함**
- [ ] 부분 채움(빈 칸) 입력 허용 여부
- [ ] 판정 출력: 통과/실패만 vs **위반 종류** 포함
- [ ] 프로젝트 맥락: 과제 / 자율 학습 / 기타
- [ ] 구현 언어·실행 환경

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [ ] defect_list.md 생성 및 발견 결함 기록
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 코드 리뷰 기반 To-Do

> code-reviewer 검토 결과 (`refactor/refactor` 기준, 2026-05-29). 우선순위 순.

### P0 — Critical (반드시 수정)

- [ ] **Entity 테스트 수집 오류 수정** — `tests/entity/test_d_*.py`가 존재하지 않는 `src.entity.services.*`를 import하여 pytest 수집 단계에서 중단됨. Boundary RED 스켈레톤(`pytest.fail`) 패턴과 동일하게 정렬
- [ ] **Golden Master 소스 복원** — `tests/golden_master/`에 `__pycache__`만 남음. `stabilize/green`에서 `.py` 소스·baseline·`pytest.ini` 복원 후 커밋
- [ ] **InputValidator GREEN 구현** — `validate_grid()` / `handle_input()`의 `NotImplementedError` 제거, AC-FR-01-01 shape 검증 완료

### P1 — Important (수정 권장)

- [ ] **ECB 레이어 정리** — Boundary가 `MagicSquareResolver`를 직접 호출하지 않도록 Control use-case(`SolveMagicSquareUseCase`) 도입
- [ ] **`MagicSquareResolver` 역할 명확화** — Control은 Entity 서비스 조합(오케스트레이션)만 담당
- [ ] **Golden Master reference → production 마이그레이션** — `reference_capture.py`의 검증·솔버 로직을 `src/entity/services/`로 이전, drift 방지
- [ ] **reference_capture 반환 타입 수정** — `_solve_two_blank_grid` 반환 타입을 `SolverResult`로 통일
- [ ] **하드코딩 제거** — `_is_magic_square`의 literal `4` → `GRID_SIZE`, `"INVALID_VALUE"` → 상수화
- [ ] **`generate_golden_master.py` `print()` 제거** — `logging`으로 대체 (프로젝트 금지 패턴)
- [ ] **Boundary 테스트 공백 보완** — BV-06 (`5×5` grid), `four_by_three` message exact match 테스트 추가
- [ ] **README 상태 갱신** — 프로젝트 상태 테이블을 RED/TDD 진행 중으로 유지

### P2 — Minor (개선)

- [ ] Boundary 테스트 literal 중복 제거 — 상수 import 후 `"INVALID_SIZE"` 등 재하드코딩 정리, parametrization 검토
- [ ] Fixture 안전성 — `[[]] * 4` → `[[] for _ in range(4)]` (행 alias 방지)
- [ ] `User` entity scaffold 정리 — 도메인과 무관하면 `examples/` 이동 또는 제거
- [ ] Entity conftest G0–G3 fixture — Boundary와 grid SSOT 통일 (`tests/conftest.py` 또는 `tests/fixtures/grids.py`)
- [ ] `pytest.ini` 복원 — `golden_master` marker 등 CI 필터 설정

### 브랜치 참고

Golden Master·partial GREEN 작업은 `stabilize/green`에 있습니다.

```powershell
git diff refactor/refactor..stabilize/green -- tests/golden_master scripts tests/integration docs/golden_master_design.md
```

---

## 다음 단계 (권장)

1. **P0 Critical** 항목부터 처리 (Entity 수집 오류 → Golden Master 복원 → InputValidator GREEN)
2. RED 체크리스트 항목 완료 및 GREEN 전환
3. P1 ECB 레이어 정리 후 Entity 서비스 구현 착수

---

## 라이선스 / 기여

미정. 프로젝트 초기 단계입니다.

---

*최종 업데이트: 2026-05-29 — RED/TDD + 코드 리뷰 To-Do 반영*
