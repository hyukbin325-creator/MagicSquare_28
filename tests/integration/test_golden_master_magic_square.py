"""GM-2 — Golden Master regression tests for Magic Square solver output."""

from __future__ import annotations

import pytest

from src.boundary.schemas import ValidationErrorResponse
from tests.golden_master.approve import (
    approve,
    approve_section,
    build_expected_document,
    read_expected,
)
from tests.golden_master.capture import (
    capture_api_result,
    capture_section_text,
    capture_stdout_result,
    serialize_api_result,
)
from tests.golden_master.constants import DEFAULT_GOLDEN_MASTER_PATH
from tests.golden_master.contract import (
    assert_duplicate_number_contract,
    assert_invalid_blank_count_contract,
    assert_no_valid_magic_square_contract,
    assert_reverse_fallback_combination,
    assert_small_first_combination,
    assert_success_output_contract,
)
from tests.golden_master.format import parse_document
from tests.golden_master.scenarios import GOLDEN_SCENARIOS, GoldenScenario


def _scenario(test_id: str) -> GoldenScenario:
    return next(item for item in GOLDEN_SCENARIOS if item.test_id == test_id)


pytestmark = pytest.mark.golden_master


class TestGoldenMasterMagicSquareDocument:
    """Full baseline document approve regression."""

    def test_golden_master_expected_file_matches_capture(self) -> None:
        actual = build_expected_document()
        approve(actual, DEFAULT_GOLDEN_MASTER_PATH)


class TestGoldenMasterMagicSquareCases:
    """GM-TC-01~05 scenario regression with contract verification."""

    def test_gm_tc_01_normal_success_combination(self) -> None:
        scenario = _scenario("GM-TC-01")
        result = capture_api_result(scenario.grid)
        assert isinstance(result, list)

        assert_success_output_contract(scenario.grid, result)
        assert_small_first_combination(scenario.grid, result)

        section_text = capture_section_text(scenario)
        approve_section(section_text, scenario.section)

    def test_gm_tc_02_reverse_success_combination(self) -> None:
        scenario = _scenario("GM-TC-02")
        result = capture_api_result(scenario.grid)
        assert isinstance(result, list)

        assert_success_output_contract(scenario.grid, result)
        assert_reverse_fallback_combination(scenario.grid, result)

        section_text = capture_section_text(scenario)
        approve_section(section_text, scenario.section)

    def test_gm_tc_03_invalid_blank_count(self) -> None:
        scenario = _scenario("GM-TC-03")
        result = capture_api_result(scenario.grid)
        assert isinstance(result, ValidationErrorResponse)

        assert_invalid_blank_count_contract(result)

        section_text = capture_section_text(scenario)
        approve_section(section_text, scenario.section)

    def test_gm_tc_04_duplicate_number(self) -> None:
        scenario = _scenario("GM-TC-04")
        result = capture_api_result(scenario.grid)
        assert isinstance(result, ValidationErrorResponse)

        assert_duplicate_number_contract(result)

        section_text = capture_section_text(scenario)
        approve_section(section_text, scenario.section)

    def test_gm_tc_05_no_valid_magic_square(self) -> None:
        scenario = _scenario("GM-TC-05")
        result = capture_api_result(scenario.grid)
        assert isinstance(result, ValidationErrorResponse)

        assert_no_valid_magic_square_contract(result)

        section_text = capture_section_text(scenario)
        approve_section(section_text, scenario.section)


class TestGoldenMasterMagicSquareCapture:
    """Output capture strategy verification."""

    @pytest.mark.parametrize("test_id", [scenario.test_id for scenario in GOLDEN_SCENARIOS])
    def test_api_serialization_matches_baseline_section(self, test_id: str) -> None:
        if not DEFAULT_GOLDEN_MASTER_PATH.exists():
            pytest.skip("Golden Master baseline file not yet generated.")

        scenario = _scenario(test_id)
        parsed = parse_document(read_expected(DEFAULT_GOLDEN_MASTER_PATH))
        section = parsed[scenario.section]
        result = capture_api_result(scenario.grid)

        if section.outcome_kind == "error":
            assert isinstance(result, ValidationErrorResponse)
            assert serialize_api_result(result) == section.outcome_lines[0]
            return

        assert isinstance(result, list)
        expected_output = section.outcome_lines[0]
        assert serialize_api_result(result) == expected_output

    @pytest.mark.parametrize("test_id", [scenario.test_id for scenario in GOLDEN_SCENARIOS])
    def test_stdout_capture_matches_api_serialization(self, test_id: str) -> None:
        scenario = _scenario(test_id)
        api_text = serialize_api_result(capture_api_result(scenario.grid))
        stdout_text = capture_stdout_result(scenario.grid)
        assert stdout_text == api_text
