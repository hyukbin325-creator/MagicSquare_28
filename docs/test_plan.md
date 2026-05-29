# MagicSquare — 테스트 계획서

| 항목 | 내용 |
|------|------|
| 문서 ID | TP-MS-001 |
| 버전 | 1.0 |
| 작성 역할 | 시니어 QA 리드 |
| 대상 요구사항 | **FR-01** Boundary 입력 검증 |
| 대표 AC | **AC-FR-01-01** — 4×4 형상 검증 |
| 대표 시나리오 | **SC-BND-VAL-004** (Level 5 보강) |
| 기술 스택 | Python 3.13+, pytest, pydantic, unittest.mock |
| 관련 Story | Story 1 — 입력 검증 (Boundary) |
| 작성일 | 2026-05-29 |

---

## 1. 목적 및 범위

### 1.1 목적

본 계획서는 **AC-FR-01-01**(입력 행렬이 유효한 4×4 형상이 아니면 `INVALID_SIZE`로 실패)을 중심으로, **pytest 기반 단위 테스트**의 범위·우선순위·경계값·Mock 전략·커버리지 목표를 정의한다.

### 1.2 In-Scope

| 구분 | 내용 |
|------|------|
| 레이어 | **Boundary** 입력 검증 (형상·크기 선행 검사) |
| 계약 | 오류 스키마 `{ code, message }`, `code = "INVALID_SIZE"`, `message = "Grid must be 4x4."` |
| 교차 검증 | 검증 실패 시 **Domain 해 결정 진입점 호출 0회** (Story 1 AC #6) |
| 구현 전제 | ECB: Boundary → Control → Entity 의존 방향 준수 |

### 1.3 Out-of-Scope (본 계획서 AC-FR-01-01 범위 외)

| 항목 | 비고 |
|------|------|
| **4×4 정상 입력** | 형상 통과 케이스 — AC-FR-01-02~05 또는 통합 시나리오에서 다룸 |
| 빈칸 개수(정확히 2개) | AC-FR-01-02 / SC-BND-VAL-001 |
| 값 범위 `0 \| 1..16` | AC-FR-01-03 / SC-BND-VAL-003 |
| `0` 제외 중복 | AC-FR-01-04 / SC-BND-VAL-002 |
| Solver 조합·마방진 합 검증 | Domain (S4, S5) — 별도 테스트 계획 |

---

## 2. 테스트 피라미드 및 레이어 전략

```text
                    ┌─────────────────────┐
                    │  통합 (소수, P2)     │  Boundary → Control → Entity (정상 1~2건)
                    └─────────────────────┘
               ┌───────────────────────────────┐
               │  Boundary 단위 (AC-FR-01, P0)  │  ← 본 계획서 핵심
               └───────────────────────────────┘
          ┌─────────────────────────────────────────┐
          │  Domain 단위 (Blank/Missing/Validator, P1) │  Mock 없이 순수 로직
          └─────────────────────────────────────────┘
```

| 레이어 | 테스트 유형 | 본 AC 관여도 | 커버리지 목표 |
|--------|---------------|--------------|---------------|
| **Boundary** | 단위 (pytest) | **주력** | **≥ 85%** |
| **Control** | 단위 + Mock Entity | 간접 (호출 차단 검증 시 Spy 대상) | ≥ 80% (프로젝트 기본) |
| **Entity (Domain)** | 단위 | AC-FR-01-01 직접 범위 아님 | **≥ 95%** |

---

## 3. pytest 단위 테스트 — 범위 및 우선순위

### 3.1 대상 모듈 (구현 예정 경로)

| 모듈 (예정) | 책임 | 테스트 파일 (예정) |
|-------------|------|-------------------|
| `src/boundary/input_validator.py` | 외부 `grid` 수신, 형상·계약 1차 검증, 오류 DTO 반환 | `tests/boundary/test_input_validator.py` |
| `src/boundary/schemas.py` | pydantic `GridInput`, `ValidationErrorResponse` | `tests/boundary/test_schemas.py` |
| `src/control/solve_magic_square.py` | Use-case 오케스트레이션, Domain 호출 | `tests/control/test_solve_magic_square.py` (호출 차단 Spy) |

> 현재 저장소는 `src/entity/user.py` 샘플만 존재한다. Magic Square Boundary/Control 구현 시 본 경로를 기준으로 테스트를 추가한다.

### 3.2 우선순위 정의

| 우선순위 | ID 접두사 | 설명 | 실행 시점 |
|----------|-----------|------|-----------|
| **P0** | `RED-BND-VAL-004-*` | AC-FR-01-01 형상 실패 + Domain 미호출 | RED 1사이클, CI 필수 |
| **P0** | `RED-BND-VAL-004-MSG` | 오류 `code`/`message` 계약 고정 | RED 1사이클, CI 필수 |
| **P1** | `RED-BND-VAL-004-EDGE` | 비정형 입력(특이 케이스) | GREEN 직후 |
| **P1** | `RED-CTL-ISO-001` | Control 경유 시 Solver/Use-case Spy | Boundary 단위 통과 후 |
| **P2** | `RED-BND-SCHEMA-*` | pydantic 파싱·타입 강제 | REFACTOR 단계 |

### 3.3 pytest 구조 (AAA)

```text
tests/
  boundary/
    test_input_validator.py      # AC-FR-01-01 형상 실패
    test_schemas.py                # pydantic 모델
  control/
    test_solve_magic_square.py     # Domain 호출 격리 (mock)
  conftest.py                      # 공통 fixture: invalid grids, spy factory
```

**Fixture 정책** (`.cursor/rules/magicsquare-tdd-testing.mdc`):

- 기본 `function` scope — 케이스 간 상태 공유 금지
- Domain Spy/Mock은 **테스트 함수마다** `unittest.mock`으로 생성·검증

### 3.4 권장 테스트 함수 명명

```text
test_ac_fr_01_01_<condition>_returns_invalid_size
test_ac_fr_01_01_<condition>_does_not_call_domain_resolver
```

---

## 4. AC-FR-01-01 — 경계값 케이스 목록

모든 케이스 공통 **기대 결과**:

| 필드 | 값 |
|------|-----|
| `code` | `"INVALID_SIZE"` |
| `message` | `"Grid must be 4x4."` |
| Domain 해 결정 진입점 호출 | **0회** |

### 4.1 P0 — 필수 경계값 (명시 요청)

| Case ID | 입력 `grid` | 실패 원인 | pytest 파라미터 ID |
|---------|-------------|-----------|-------------------|
| **BV-01** | `None` | 참조 없음 — 형상 미정의 | `none` |
| **BV-02** | `[]` | 행 0개 | `empty_list` |
| **BV-03** | `[[]] * 4` | 행 4, 열 0 (`len(row) != 4`) | `four_rows_zero_cols` |
| **BV-04** | `3×4` 행렬 (3행×4열) | `len(grid) != 4` | `three_by_four` |
| **BV-05** | `4×3` 행렬 (4행×3열) | 열 길이 불일치 | `four_by_three` |
| **BV-06** | `5×5` 행렬 | `len(grid) != 4` | `five_by_five` |

#### BV-01 ~ BV-06 입력 예시 (Arrange)

```python
# BV-01
grid = None

# BV-02
grid = []

# BV-03  — 주의: [[]]*4는 동일 빈 리스트 참조 4개 (의도된 엣지)
grid = [[]] * 4

# BV-04  (3×4)
grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# BV-05  (4×3)
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

# BV-06  (5×5) — 값은 더미, 형상만 검증
grid = [[0] * 5 for _ in range(5)]
```

### 4.2 명시적 제외 (본 AC 범위 외)

| Case ID | 입력 | 제외 사유 |
|---------|------|-----------|
| **EX-01** | 유효한 **4×4** 행렬 (빈칸 2개 등) | AC-FR-01-01은 **실패** 경로만 대상; 통과는 AC-FR-01-02 이후 또는 통합 테스트 |

> **EX-01**은 회귀 스위트에는 포함하되, **AC-FR-01-01 전용 테스트 모듈/파라미터 세트에는 포함하지 않는다.**

### 4.3 P1 — 추가 형상 경계 (권장)

| Case ID | 입력 | 실패 원인 |
|---------|------|-----------|
| BV-07 | `[[1,2,3,4]]` (1×4) | 행 1개 |
| BV-08 | `[[1],[2],[3],[4]]` (4×1) | 열 1개 |
| BV-09 | 행 길이 혼합 `[4열, 3열, 4열, 4열]` | 비직사각형 |
| BV-10 | `[[1,2,3,4,5]]*4` (4×5) | 열 초과 |

---

## 5. 예외·특이 케이스 목록

| Case ID | 입력 / 조건 | 기대 동작 | 우선순위 | 비고 |
|---------|-------------|-----------|----------|------|
| **EXC-01** | `grid`가 `list`가 아님 (`"4x4"`, `42`, `4.0`) | `INVALID_SIZE` (또는 pydantic `ValidationError` → Boundary가 동일 계약으로 매핑) | P1 | 타입 계약 |
| **EXC-02** | `grid` 내부 행이 `list`가 아님 (`[1,2,3,4]` 1차원) | `INVALID_SIZE` | P1 | jagged/flat 혼동 방지 |
| **EXC-03** | `grid`에 `None` 행 포함 (`[None, [], [], []]`) | `INVALID_SIZE` | P1 | |
| **EXC-04** | 셀 값이 `None` / `float` / `str` | **AC-FR-01-01 아님** — 값 범위 AC-FR-01-03에서 처리; 형상 검사만 통과한 뒤 후속 AC에서 실패 | P2 | 교차 오염 방지: 형상 테스트 데이터는 **정수 리스트**만 사용 |
| **EXC-05** | `[[]]*4` 후 한 행만 `append`로 변형 | 나머지 행仍 0열 — **BV-03** 회귀 | P1 | Python 참조 공유 특성 |
| **EXC-06** | 매우 큰 중첩 리스트 (메모리·DoS) | `INVALID_SIZE` 또는 조기 거부; **시간 상한** assert (예: &lt; 100ms) | P2 | 비기능 |
| **EXC-07** | Boundary가 pydantic `GridInput` 사용 시, `None` → validator 전 **명시적 None 가드** | `ValidationError` 미발생하고 계약 오류 DTO 반환 | P0 | `None`은 pydantic v2에서 별도 처리 필요 |

### 5.1 pydantic 사용 시 정책

- **형상 검사 순서:** `grid is None` → 행/열 길이 → (선택) pydantic 모델
- `None`을 모델 필드에 넣기 전 **Boundary에서 1차 처리**하여, AC-FR-01-01 메시지가 항상 `"Grid must be 4x4."`로 고정되도록 한다.
- 오류 응답 모델 예: `ValidationErrorResponse(code: Literal["INVALID_SIZE", ...], message: str)`

---

## 6. Domain 해 결정 진입점 — 호출 횟수 검증 전략

### 6.1 검증 대상 (Spy/Mock 대상)

| 진입점 (예정 이름) | 레이어 | 설명 |
|-------------------|--------|------|
| `SolveMagicSquareUseCase.execute` | Control | Boundary 통과 후 Domain 오케스트레이션 |
| `MagicSquareSolver.solve` | Entity/Domain | 최종 해 결정 |
| `BlankFinder.find` / `MissingNumberFinder.find` | Entity | (선택) 세분 Spy |

**AC-FR-01-01 관점의 단일 관찰점:** Control의 `execute` 또는 Solver `solve` **1곳**을 표준으로 고정한다.

### 6.2 패턴 A — Boundary 단위 + Mock Control (권장 P0)

```text
Given  invalid grid (BV-01 ~ BV-06)
When   BoundaryValidator.validate(grid)  또는  BoundaryFacade.solve(grid)
Then   result.code == "INVALID_SIZE"
And    mock_control.execute.call_count == 0
```

- **방법:** `unittest.mock.MagicMock(spec=SolveMagicSquareUseCase)`를 Boundary 생성자에 DI
- **장점:** Domain/Control 구현 없이 RED 가능 (Dual-Track UI Track)

### 6.3 패턴 B — Control 단위 + Spy Entity (P1)

```text
Given  invalid grid
When   use_case.execute(grid)   # Boundary 검증을 Control 앞단에 둔 경우
Then   mock_solver.solve.call_count == 0
```

- Boundary와 Control 책임이 한 함수에 있을 경우, **검증 실패 분기 직후** return 되는지 코드 경로 커버리지로 보완

### 6.4 패턴 C — `pytest-mock` / `mocker.spy` (선택)

```text
mocker.spy(solver, "solve")
# ... act ...
assert solver.solve.call_count == 0
```

- **주의:** spy는 실제 메서드를 호출할 수 있으므로, **invalid 입력에서는 Mock(`autospec=True`)** 을 P0 기본으로 한다.

### 6.5 검증 체크리스트 (AC-FR-01-05 / Story 1 AC #6)

| # | 검증 항목 | 도구 |
|---|-----------|------|
| 1 | `execute` / `solve` 호출 0회 | `assert_called_once` **부정** → `assert not mock.called` |
| 2 | 하위 Finder/Validator도 미호출 | 동일 Mock 트리에 바인딩 |
| 3 | 예외 전파 없이 오류 DTO 반환 | `pytest.raises` **사용 안 함** (계약은 반환형) |
| 4 | Mock이 실제 네트워크/파일 접근 없음 | 단위 테스트 격리 |

### 6.6 conftest 공통 Fixture (권장)

| Fixture | 역할 |
|---------|------|
| `mock_use_case` | `MagicMock(spec=SolveMagicSquareUseCase)` |
| `boundary_with_mock_control` | DI된 Boundary 인스턴스 |
| `invalid_size_grids` | BV-01~06 파라미터 소스 |

---

## 7. 테스트 케이스 ↔ 추적성 매트릭스

| Test ID | AC | Scenario | 입력 | 기대 `code` | Domain 호출 |
|---------|-----|----------|------|-------------|-------------|
| RED-BND-VAL-004-01 | AC-FR-01-01 | SC-BND-VAL-004 | `None` | INVALID_SIZE | 0 |
| RED-BND-VAL-004-02 | AC-FR-01-01 | SC-BND-VAL-004 | `[]` | INVALID_SIZE | 0 |
| RED-BND-VAL-004-03 | AC-FR-01-01 | SC-BND-VAL-004 | `[[]]*4` | INVALID_SIZE | 0 |
| RED-BND-VAL-004-04 | AC-FR-01-01 | SC-BND-VAL-004 | 3×4 | INVALID_SIZE | 0 |
| RED-BND-VAL-004-05 | AC-FR-01-01 | SC-BND-VAL-004 | 4×3 | INVALID_SIZE | 0 |
| RED-BND-VAL-004-06 | AC-FR-01-01 | SC-BND-VAL-004 | 5×5 | INVALID_SIZE | 0 |

---

## 8. 커버리지 목표

### 8.1 레이어별 목표 (Epic 성공 기준)

| 레이어 | 목표 | 측정 패키지 (예정) | AC-FR-01-01 기여 |
|--------|------|-------------------|------------------|
| **Domain (Entity)** | **≥ 95%** | `src/entity` | 간접 (Boundary에서 차단) |
| **Boundary** | **≥ 85%** | `src/boundary` | **직접 — 본 계획 핵심** |
| **Control** | ≥ 80% | `src/control` | `execute` 조기 return 분기 |
| **프로젝트 전체** | ≥ 80% | `src` | `.cursorrules` 기본선 |

### 8.2 AC-FR-01-01 구현 시 필수 커버 분기

- `grid is None`
- `len(grid) != GRID_SIZE`
- `any(len(row) != GRID_SIZE for row in grid)`
- 검증 실패 시 Domain/Control **미호출** return 경로

### 8.3 커버리지에서 제외·별도 관리

| 항목 | 처리 |
|------|------|
| 4×4 정상 통과 경로 | AC-FR-01-01 전용 `--cov` 실행 시 제외 가능; 전체 스위트에서는 포함 |
| `pragma: no cover` | 디버그·불가능 방어 코드만, QA 승인 후 |

---

## 9. pytest-cov 측정 전략

### 9.1 설치

```bash
pip install pytest-cov
```

개발 의존성으로 고정 시 (권장):

```text
# requirements-dev.txt (예시)
pytest>=8.0
pytest-cov>=5.0
pydantic>=2.0
```

### 9.2 기본 실행 (전체)

```bash
pytest --cov=src --cov-report=term-missing
```

### 9.3 AC-FR-01-01 집중 실행 (Boundary만)

```bash
pytest tests/boundary/test_input_validator.py \
  --cov=src/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 9.4 Domain 집중 실행

```bash
pytest tests/entity tests/control \
  --cov=src/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 9.5 CI 권장 (분리 잡)

| Job | 명령 | 실패 조건 |
|-----|------|-----------|
| `test-boundary` | `pytest tests/boundary --cov=src/boundary --cov-fail-under=85` | Boundary &lt; 85% |
| `test-domain` | `pytest tests/entity --cov=src/entity --cov-fail-under=95` | Domain &lt; 95% |
| `test-all` | `pytest --cov=src --cov-report=xml` | 전체 &lt; 80% |

### 9.6 커버리지 해석 주의

| 현상 | 대응 |
|------|------|
| Boundary만 구현 시 Domain 0% | Domain RED 전에는 `test-domain` 잡 **skip** 또는 최소 스텁 |
| Mock으로 Control을 대체 | Boundary 모듈의 **실패 분기**는 100%에 가깝게 유지 |
| `term-missing` 미커버 라인 | AC-FR-01-01 미구현 분기 우선 구현 |

### 9.7 (선택) `pyproject.toml` 설정 예시

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## 10. 실행 순서 (TDD RED → GREEN)

| 단계 | 활동 | 산출 |
|------|------|------|
| 1 RED | BV-01 (`None`) 단일 테스트 + Mock Control | 실패 확인 |
| 2 RED | BV-02~06 `@pytest.mark.parametrize` | 형상 실패 일괄 RED |
| 3 RED | `message`/`code` 정확 일치 assert | 계약 고정 |
| 4 GREEN | `InputValidator` 최소 구현 | 통과 |
| 5 RED | EXC-01~03 특이 케이스 | 보강 |
| 6 GREEN | 타입 가드·None 가드 | |
| 7 REFACTOR | `GRID_SIZE` 상수 추출, pydantic 모델 정리 | 커버리지 유지 |
| 8 | `pytest --cov=src/boundary --cov-fail-under=85` | Boundary 목표 달성 보고 |

---

## 11. 완료 정의 (Definition of Done) — AC-FR-01-01

- [ ] BV-01 ~ BV-06 전부 통과, `code`/`message` 계약 일치
- [ ] 각 BV 케이스에서 Domain 해 결정 진입점 **호출 0회** 검증
- [ ] **4×4 정상 입력**이 AC-FR-01-01 전용 테스트에 **포함되지 않음** (EX-01 준수)
- [ ] `src/boundary` 커버리지 **≥ 85%** (`pytest-cov` 증빙)
- [ ] ECB 역방향 의존 없음 (Entity → Boundary import 없음)
- [ ] `print()` 미사용, 상수명 `GRID_SIZE` 등 명명 규칙 준수

---

## 12. 참고 문서

| 문서 | 경로 |
|------|------|
| Level 1~5 Export | `Report/06.MagicSquare-Level1-5-Export-Report.md` |
| PRD 참고 분석 | `Report/07.PRD-Reference-Analysis-Export-Report.md` |
| ECB 규칙 | `.cursor/rules/magicsquare-ecb-architecture.mdc` |
| TDD 규칙 | `.cursor/rules/magicsquare-tdd-testing.mdc` |

---

## 문서 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.0 | 2026-05-29 | 초안 — AC-FR-01-01 중심 테스트 계획 |
