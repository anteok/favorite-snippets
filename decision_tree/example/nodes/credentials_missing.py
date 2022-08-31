from enum import Enum
from typing import Union

from decision_tree.example.base import (
    ValidationNode,
    ValidationSwitch,
)
from decision_tree.example.entities import SessionDto, ValidationDecision, BinaryRange


class CredentialsMissingNode(ValidationNode):
    """Checks if username and pass hash are provided."""

    def _validate(self, dto: SessionDto) -> Enum:
        if dto.user_name and dto.pass_hash:
            return BinaryRange.positive
        return BinaryRange.negative


class CredentialsMissingOptionsSwitch(ValidationSwitch):
    def _get_result(
        self, dto: SessionDto, decision_option: Enum
    ) -> Union[ValidationNode, ValidationDecision]:
        if decision_option is BinaryRange.positive:
            return self._container.user_exists
        elif decision_option is BinaryRange.negative:
            return ValidationDecision(valid=False)
        raise AssertionError("Wrong enum is used, BinaryRange required")
