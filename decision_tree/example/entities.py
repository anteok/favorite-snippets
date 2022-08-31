from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from decision_tree.base import BaseDto, Decision


@dataclass
class SessionDto(BaseDto):
    """A simplified example of aggregated user data."""

    device_session_id: str
    auth_required: bool
    user_name: Optional[str] = None
    pass_hash: Optional[str] = None

    _user_exists_in_db: bool = True

    def is_user_exists(self) -> bool:
        """Checks user database record existence."""
        return self._user_exists_in_db

    def is_session_valid(self) -> bool:
        """Any kind of checking session validity."""
        return bool(self.device_session_id)


@dataclass
class ValidationDecision(Decision):
    """Decision of validation"""

    valid: bool


class BinaryRange(Enum):
    """Binary decision range."""

    positive = "positive"
    negative = "negative"
