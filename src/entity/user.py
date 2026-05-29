"""User entity for the MagicSquare domain."""

from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class User:
    """Represent a user in the domain model.

    Attributes:
        user_id: Unique identifier for the user.
        username: Display name used inside the system.
        email: Contact email for the user.
        is_active: Activation state of the user.
    """

    user_id: int
    username: str
    email: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate entity invariants at creation time.

        Raises:
            ValueError: If any field violates domain constraints.
        """
        if self.user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not self.username.strip():
            raise ValueError("Username must not be blank")
        if "@" not in self.email:
            raise ValueError("Email must contain '@'")

    def deactivate(self) -> "User":
        """Return a new user marked as inactive.

        Returns:
            User: A copied instance with ``is_active=False``.
        """
        return replace(self, is_active=False)

    def activate(self) -> "User":
        """Return a new user marked as active.

        Returns:
            User: A copied instance with ``is_active=True``.
        """
        return replace(self, is_active=True)

    def rename(self, new_username: str) -> "User":
        """Return a new user with an updated username.

        Args:
            new_username: New username value to apply.

        Returns:
            User: A copied instance with the updated username.

        Raises:
            ValueError: If ``new_username`` is blank.
        """
        if not new_username.strip():
            raise ValueError("Username must not be blank")
        return replace(self, username=new_username)
