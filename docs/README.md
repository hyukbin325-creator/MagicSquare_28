# MagicSquare — 문서 인덱스

프로젝트 루트 [README.md](../README.md) · [test_plan.md](test_plan.md) · [golden_master_design.md](golden_master_design.md)

---

## RED 단계 To-Do 리스트

Track A/B RED·GREEN 진행, 커버리지, `defect_list` 연동은 [test_plan.md](test_plan.md) 및 루트 [README.md](../README.md) § RED / GREEN 체크리스트를 SSOT로 따른다.

### Track A — Boundary

- [ ] A-1: `handle_input(None)` + resolve 격리
- [ ] A-2~A-5: `[]`, 4×0열, 3×4, 4×3 형상 실패
- [ ] A-6~A-8: U-IN / U-OUT / U-FLOW 스켈레톤 GREEN

### Track B — Entity

- [ ] B-0: `src/entity/services/` 패키지 생성
- [ ] B-1~B-7: D-LOC / D-MIS / D-VAL / D-SOL GREEN

### 커버리지 · 기타

- [ ] Domain 95%+ · Boundary 85%+ · 전체 80%+
- [ ] `defect_list.md` 결함 추적
- [ ] GUI 수동 확인 (`boundary/screen/`)

---

## Golden Master 회귀 안전장치

Refactoring 시작 전 구축.  
GREEN 완료 후 즉시 적용.

### 기준 파일 생성

- GM-01: `golden_master_expected.txt` 생성
- GM-02: 정상/역순/오류 시나리오 추가
- GM-03: `git add tests/golden_master_expected.txt`

### 테스트 코드

- GM-04: `test_golden_master_magic_square` 작성
- GM-05: approve 패턴 적용
- GM-06: Golden Master 테스트 PASS 확인

```bash
python -m pytest -m golden_master -v
```

### 회귀 보호

- GM-07: row-major 규칙 보호
- GM-08: 1-index 출력 보호
- GM-09: reverse 조합 fallback 보호
- GM-10: Error Contract 보호

관련 경로: `tests/golden_master_expected.txt` · `tests/integration/test_golden_master_magic_square.py` · `scripts/generate_golden_master.py`
