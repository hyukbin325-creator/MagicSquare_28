"""Pydantic models for Boundary validation responses."""

from pydantic import BaseModel, ConfigDict


class ValidationErrorResponse(BaseModel):
    """Failure result returned when input validation fails at the Boundary."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str
