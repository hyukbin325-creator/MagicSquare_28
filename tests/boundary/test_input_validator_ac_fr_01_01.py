"""AC-FR-01-01, PRD §8.1 INVALID_SIZE — 4×4 형상 검증 RED 테스트."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.boundary.constants import GRID_SHAPE_ERROR_MESSAGE, INVALID_SIZE_CODE
from src.boundary.input_validator import InputValidator
from src.boundary.schemas import ValidationErrorResponse
from tests.boundary.conftest import INVALID_SHAPE_GRIDS, OUT_OF_SCOPE_GRIDS


class TestAcFr0101NormalFailureReturn:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 정상 실패 반환."""

    def test_none_grid_returns_invalid_size_failure_result(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        result = validator.validate_grid(grid)
        # Then
        assert isinstance(result, ValidationErrorResponse)
        assert result.code == INVALID_SIZE_CODE

    def test_none_grid_returns_validation_error_response_type(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        result = validator.validate_grid(grid)
        # Then
        assert type(result) is ValidationErrorResponse

    def test_none_grid_does_not_return_success_list_payload(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        result = validator.handle_input(grid)
        # Then
        assert isinstance(result, ValidationErrorResponse)
        assert not isinstance(result, list)

    def test_none_grid_failure_result_code_field_is_invalid_size(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.code == "INVALID_SIZE"

    def test_none_grid_failure_result_message_field_is_prd_shape_text(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.message == GRID_SHAPE_ERROR_MESSAGE


class TestAcFr0101BoundaryValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 경계값 형상 실패."""

    def test_empty_list_grid_returns_invalid_size_code(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE

    def test_four_rows_zero_cols_grid_returns_invalid_size_code(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = [[]] * 4
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE

    def test_three_by_four_grid_returns_invalid_size_code(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = INVALID_SHAPE_GRIDS["three_by_four"]
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE

    def test_four_by_three_grid_returns_invalid_size_code(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = INVALID_SHAPE_GRIDS["four_by_three"]
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.code == INVALID_SIZE_CODE

    def test_empty_list_grid_returns_validation_error_response_type(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []
        # When
        result = validator.validate_grid(grid)
        # Then
        assert isinstance(result, ValidationErrorResponse)


class TestAcFr0101ResolverIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Domain resolve() 호출 격리."""

    def test_none_grid_resolve_call_count_zero(
        self, validator: InputValidator, mock_resolver: MagicMock
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        validator.handle_input(grid)
        # Then
        mock_resolver.resolve.assert_not_called()

    def test_empty_list_grid_resolve_call_count_zero(
        self, validator: InputValidator, mock_resolver: MagicMock
    ) -> None:
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []
        # When
        validator.handle_input(grid)
        # Then
        mock_resolver.resolve.assert_not_called()

    def test_four_rows_zero_cols_grid_resolve_call_count_zero(
        self, validator: InputValidator, mock_resolver: MagicMock
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = [[]] * 4
        # When
        validator.handle_input(grid)
        # Then
        mock_resolver.resolve.assert_not_called()

    def test_three_by_four_grid_resolve_call_count_zero(
        self, validator: InputValidator, mock_resolver: MagicMock
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = INVALID_SHAPE_GRIDS["three_by_four"]
        # When
        validator.handle_input(grid)
        # Then
        mock_resolver.resolve.assert_not_called()

    def test_none_grid_resolve_never_receives_none_argument(
        self, validator: InputValidator, mock_resolver: MagicMock
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        # When
        validator.handle_input(grid)
        # Then
        for call in mock_resolver.resolve.call_args_list:
            assert call.args[0] is not None


class TestAcFr0101MessageExactMatch:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 오류 문구 문자 단위 일치."""

    def test_none_grid_message_exact_match_prd_section_8_1(
        self, validator: InputValidator, prd_shape_error_message: str
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        expected_message = "Grid must be 4x4."
        assert prd_shape_error_message == expected_message
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.message == expected_message

    def test_empty_list_message_exact_match_prd_section_8_1(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid: list[list[int]] = []
        expected_message = "Grid must be 4x4."
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.message == expected_message

    def test_four_rows_zero_cols_message_exact_match_prd_section_8_1(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = [[]] * 4
        expected_message = "Grid must be 4x4."
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.message == expected_message

    def test_three_by_four_message_exact_match_prd_section_8_1(
        self, validator: InputValidator
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = INVALID_SHAPE_GRIDS["three_by_four"]
        expected_message = "Grid must be 4x4."
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.message == expected_message

    def test_none_grid_code_exact_match_invalid_size_literal(
        self, validator: InputValidator, prd_invalid_size_code: str
    ) -> None:
        # AC-FR-01-01
        # Given
        grid = None
        expected_code = "INVALID_SIZE"
        assert prd_invalid_size_code == expected_code
        # When
        result = validator.validate_grid(grid)
        # Then
        assert result is not None
        assert result.code == expected_code


class TestAcFr0101ScopeLimitation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 / FR-02~05 범위 제한."""

    def test_scope_fixtures_exclude_valid_4x4_two_blanks(self) -> None:
        # AC-FR-01-01
        # Given
        out_of_scope = OUT_OF_SCOPE_GRIDS["valid_4x4_two_blanks"]
        # When / Then
        assert out_of_scope not in INVALID_SHAPE_GRIDS.values()

    def test_scope_fixtures_exclude_four_by_four_one_blank_ac_fr_01_02(self) -> None:
        # AC-FR-01-01
        # Given
        blank_count_case = OUT_OF_SCOPE_GRIDS["four_by_four_one_blank"]
        # When / Then
        assert blank_count_case not in INVALID_SHAPE_GRIDS.values()

    def test_scope_fixtures_exclude_four_by_four_duplicate_ac_fr_01_04(self) -> None:
        # AC-FR-01-01
        # Given
        duplicate_case = OUT_OF_SCOPE_GRIDS["four_by_four_duplicate"]
        # When / Then
        assert duplicate_case not in INVALID_SHAPE_GRIDS.values()

    def test_scope_fixtures_exclude_four_by_four_out_of_range_ac_fr_01_03(self) -> None:
        # AC-FR-01-01
        # Given
        range_case = OUT_OF_SCOPE_GRIDS["four_by_four_out_of_range"]
        # When / Then
        assert range_case not in INVALID_SHAPE_GRIDS.values()

    def test_scope_invalid_shape_keys_only_cover_ac_fr_01_01_shape_cases(self) -> None:
        # AC-FR-01-01
        # Given
        allowed_keys = {
            "none",
            "empty_list",
            "four_rows_zero_cols",
            "three_by_four",
            "four_by_three",
        }
        # When / Then
        assert set(INVALID_SHAPE_GRIDS.keys()) == allowed_keys
