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
from enum import Enum
from typing import Union

from decision_tree.base import (
    AbstractNode,
    BaseDto,
    Decision,
    DecisionSwitch,
    SwitchedNode,
)
from decision_tree.example.entities import SessionDto, ValidationDecision


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
