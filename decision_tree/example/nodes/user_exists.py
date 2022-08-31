from enum import Enum
from typing import Union

from decision_tree.example.base import (
    ValidationNode,
    ValidationSwitch,
)
from decision_tree.example.entities import SessionDto, ValidationDecision, BinaryRange


class UserExistsNode(ValidationNode):
    """Checks if user exists in db."""

    def _validate(self, dto: SessionDto) -> Enum:
        return BinaryRange.positive if dto.is_user_exists() else BinaryRange.negative


class UserExistsOptionsSwitch(ValidationSwitch):
    def _get_result(
        self, dto: SessionDto, decision_option: Enum
    ) -> Union[ValidationNode, ValidationDecision]:
        if decision_option is BinaryRange.positive:
            return self._container.is_session_valid
        elif decision_option is BinaryRange.negative:
            return ValidationDecision(valid=False)
        raise AssertionError("Wrong enum is used, BinaryRange required")
