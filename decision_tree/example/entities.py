"""An example of usage based on simplified authentication validation process.

A decision tree nodes could be described with these statements:
1. If authentication is required, then go to 2, else go to 4.
2. If username is missing or pass_hash is missing, then user is invalid, else go to 3
3. If user record exists in database, then go to 4, else user is invalid
4. If device session is valid, then user is valid, else user is invalid.

This is not a production-ready example! Of course, real user validation is much more complicated,
and also, possibly, such an insignificant amount of checks requires a lot of boilerplate code there.
That example illustrates how it can be applied to any kind of tree architectures.
"""
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from decision_tree.base import (
    AbstractNode,
    AbstractTreeContainer,
    BaseDto,
    Decision,
    DecisionSwitch,
    SwitchedNode,
)
from decision_tree.example.nodes.credentials_missing import (
    CredentialsMissingNode,
    CredentialsMissingOptionsSwitch,
)
from decision_tree.example.nodes.is_auth_required import (
    IsAuthRequiredNode,
    IsAuthRequiredOptionsSwitch,
)
from decision_tree.example.nodes.is_session_valid import (
    IsSessionValid,
    IsSessionValidOptionsSwitch,
)
from decision_tree.example.nodes.user_exists import (
    UserExistsNode,
    UserExistsOptionsSwitch,
)


@dataclass
class SessionDto(BaseDto):
    """A simplified example of aggregated user data."""

    device_session_id: str
    auth_required: bool
    user_name: Optional[str] = None
    pass_hash: Optional[str] = None

    def is_user_exists(self) -> bool:
        """Checks user database record existence."""
        return True

    def is_session_valid(self) -> bool:
        """Any kind of checking session validity."""
        return True


@dataclass
class ValidationDecision(Decision):
    """Decision of validation"""

    valid: bool


class BinaryRange(Enum):
    """Binary decision range."""

    positive = "positive"
    negative = "negative"


class ValidationNode(SwitchedNode):
    """Overload of basic class for checking signatures.

    It may be skipped in real life :)
    """

    def _decide(self, dto: BaseDto) -> Enum:
        if not isinstance(dto, SessionDto):
            raise AssertionError("SessionDto object must be used!")
        return self._validate(dto)

    @abstractmethod
    def _validate(self, dto: SessionDto) -> Enum:
        raise NotImplementedError


class ValidationSwitch(DecisionSwitch):
    """Overload of basic class for checking signatures.

    It may be skipped in real life :)
    """

    def get_result(
        self, dto: BaseDto, decision_option: Enum
    ) -> Union[AbstractNode, Decision]:
        if not isinstance(dto, SessionDto):
            raise AssertionError("SessionDto object must be used!")
        return self._get_result(dto, decision_option)

    @abstractmethod
    def _get_result(
        self, dto: SessionDto, decision_option: Enum
    ) -> Union[ValidationNode, ValidationDecision]:
        raise NotImplementedError


class ValidationTreeContainer(AbstractTreeContainer):
    """Container with initialized nodes."""

    def __init__(self):
        self.auth_required_node = IsAuthRequiredNode(
            decision_switch=IsAuthRequiredOptionsSwitch(self),
        )
        self.credential_missing_node = CredentialsMissingNode(
            decision_switch=CredentialsMissingOptionsSwitch(self),
        )
        self.user_exists = UserExistsNode(
            decision_switch=UserExistsOptionsSwitch(self),
        )
        self.is_session_valid = IsSessionValid(
            decision_switch=IsSessionValidOptionsSwitch(self),
        )
        self._initial_node = self.auth_required_node
