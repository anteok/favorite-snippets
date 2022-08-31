from enum import Enum
from typing import Union

from decision_tree.example.entities import (
    BinaryRange,
    SessionDto,
    ValidationDecision,
    ValidationNode,
    ValidationSwitch,
)


class IsSessionValid(ValidationNode):
    """Checks if user session is valid."""

    def _validate(self, dto: SessionDto) -> Enum:
        return BinaryRange.positive if dto.is_session_valid() else BinaryRange.negative


class IsSessionValidOptionsSwitch(ValidationSwitch):
    def _get_result(
        self, dto: SessionDto, decision_option: Enum
    ) -> Union[ValidationNode, ValidationDecision]:
        if decision_option is BinaryRange.positive:
            return ValidationDecision(valid=True)
        elif decision_option is BinaryRange.negative:
            return ValidationDecision(valid=False)
        raise AssertionError("Wrong enum is used, BinaryRange required")
