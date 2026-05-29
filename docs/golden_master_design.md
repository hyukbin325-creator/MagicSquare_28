# Golden Master (GM-1) — Approve 패턴 설계

| 항목 | 내용 |
|------|------|
| 문서 ID | GM-MS-001 |
| 대상 | Magic Square Solver 출력 회귀 (Approval / Golden Master) |
| 기준 파일 | `tests/golden_master_expected.txt` |
| 생성 스크립트 | `scripts/generate_golden_master.py` |
| 비교 유틸 | `tests/golden_master/approve.py` |
| 회귀 테스트 | `tests/integration/test_golden_master_magic_square.py` |

---

## 1. 목적

Solver(또는 Boundary `handle_input` 경로)의 **결과 DTO**를 고정된 텍스트 기준선과 비교해, 출력 계약이 의도치 않게 바뀌면 **unified diff**와 함께 테스트를 실패시킨다.

- 성공: `list[int]` — `[r1, c1, n1, r2, c2, n2]` (1-index)
- 실패: `ValidationErrorResponse.code` — 한 줄 오류 코드

stdout 캡처는 CLI가 없으므로 **DTO 직렬화**를 기본 전략으로 사용한다.

---

## 2. 기준 파일 구조

섹션은 `________________________________________` 로 구분한다.

```text
[normal_success]
Input:
16 2 3 13
...
Output:
[3,2,7,4,4,1]
________________________________________

[reverse_success]
...
Output:
[3,3,6,4,4,1]
________________________________________

[invalid_blank_count]
...
Error:
INVALID_BLANK_COUNT
```

### 시나리오 SSOT

| 섹션 | 격자 키 | 의미 | 기대 결과 |
|------|---------|------|-----------|
| `normal_success` | G2 | small-first 조합 성공 | 6-튜플 Output |
| `reverse_success` | G0 | reverse 조합 성공 (G0에서 small-first 실패) | `[3,3,6,4,4,1]` |
| `invalid_blank_count` | `four_by_four_one_blank` | 빈칸 ≠ 2 | `INVALID_BLANK_COUNT` |
| `duplicate_number` | `four_by_four_duplicate` | 0 제외 중복 | `DUPLICATE_NUMBER` |
| `no_valid_magic_square` | G3 | 2빈칸·양 조합 모두 불변식 실패 | `NO_VALID_MAGIC_SQUARE` |

격자 정의: `tests/golden_master/scenarios.py`

---

## 3. Approve 패턴

```text
                    ┌─────────────────────────┐
                    │ capture_solver_result() │
                    │ (reference / production)│
                    └───────────┬─────────────┘
                                │
                    build_expected_document()
                                │
                                ▼
                    ┌─────────────────────────┐
     없음 ────────► │ golden_master_expected  │ ──► FAIL (1회): baseline 생성 안내
                    │ .txt 존재?              │
                    └───────────┬─────────────┘
                          있음  │
                                ▼
                    actual == expected ?
                      │ yes          │ no
                      ▼              ▼
                   PASS          unified diff + FAIL
```

### 동작 규칙

1. **기준 파일 없음** (`approve()` 첫 호출): 현재 캡처를 파일에 쓰고 `pytest.fail` — “baseline 생성됨, 재실행하라”는 1회성 신호.
2. **기준 파일 있음**: 전체 문서 문자열 equality 비교.
3. **불일치**: `difflib.unified_diff` 를 assertion 메시지에 포함 후 FAIL.

생성 전용 경로는 `write_baseline()` — 스크립트/로컬 갱신 시 사용, 테스트 실패 없이 덮어씀.

---

## 4. 캡처 전략

| 단계 | 구현 | 비고 |
|------|------|------|
| 현재 (GM-1) | `tests/golden_master/reference_capture.py` | Entity Solver GREEN 전 bootstrap용 reference |
| 이후 | `InputValidator.handle_input()` + 실제 `MagicSquareResolver` | ECB 스택 GREEN 후 `capture_solver_result` 교체 |

Reference capture는 PRD와 동일한 규칙을 따른다.

- 빈칸 row-major 순서
- missing 숫자 오름차순 → small-first, 그 다음 reverse
- 마방 상수 34 검증

---

## 5. 운영 절차

### 기준 파일 최초 생성 / 갱신

```bash
python scripts/generate_golden_master.py
git add tests/golden_master_expected.txt
```

### 회귀 검증

```bash
python -m pytest -m golden_master -v
# 또는
python -m pytest tests/integration/test_golden_master_magic_square.py -m golden_master -v
```

### 의도적 출력 변경

1. Solver/계약 변경 구현
2. `python scripts/generate_golden_master.py` 로 baseline 재생성
3. diff 리뷰 후 `golden_master_expected.txt` 커밋

---

## 6. ECB 및 TDD 정합

- Golden Master 테스트는 **integration** 레이어 — Boundary~Entity 관통 결과를 검증.
- Reference capture는 `tests/` 전용; `src/entity` 미구현 시에도 GM-1 baseline 고정 가능.
- Domain GREEN 후 reference를 production resolver로 교체해도 **기준 파일은 동일**해야 한다 (불일치 시 diff로 드러남).

---

## 7. 관련 파일

| 경로 | 역할 |
|------|------|
| `tests/golden_master_expected.txt` | 버전 관리되는 expected 출력 |
| `scripts/generate_golden_master.py` | baseline 생성 CLI |
| `tests/golden_master/format.py` | 섹션 파싱/직렬화 |
| `tests/golden_master/approve.py` | approve / write_baseline |
| `tests/golden_master/reference_capture.py` | DTO 캡처 (bootstrap) |
| `tests/integration/test_golden_master_magic_square.py` | GM-TC-01~05 회귀 테스트 |
