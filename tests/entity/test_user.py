"""Tests for the User entity."""

import pytest

from src.entity.user import User


def test_create_user_sets_expected_defaults() -> None:
    """Create a user with valid fields."""
    # Arrange
    user_id = 1
    username = "alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, username=username, email=email)

    # Assert
    assert user.user_id == user_id
    assert user.username == username
    assert user.email == email
    assert user.is_active is True


def test_create_user_with_invalid_email_raises_value_error() -> None:
    """Reject a user when email format is invalid."""
    # Arrange
    invalid_email = "alice-example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="Email must contain '@'"):
        User(user_id=1, username="alice", email=invalid_email)


def test_deactivate_returns_inactive_user() -> None:
    """Return a new inactive user instance."""
    # Arrange
    user = User(user_id=1, username="alice", email="alice@example.com")

    # Act
    updated_user = user.deactivate()

    # Assert
    assert updated_user.is_active is False
    assert user.is_active is True


def test_rename_returns_user_with_new_username() -> None:
    """Return a new user instance with updated username."""
    # Arrange
    user = User(user_id=1, username="alice", email="alice@example.com")
    new_username = "alice_2"

    # Act
    updated_user = user.rename(new_username)

    # Assert
    assert updated_user.username == new_username
    assert updated_user.user_id == user.user_id
    assert updated_user.email == user.email
    assert updated_user.is_active == user.is_active


def test_rename_with_blank_username_raises_value_error() -> None:
    """Reject rename when the username is blank."""
    # Arrange
    user = User(user_id=1, username="alice", email="alice@example.com")

    # Act / Assert
    with pytest.raises(ValueError, match="Username must not be blank"):
        user.rename("   ")
