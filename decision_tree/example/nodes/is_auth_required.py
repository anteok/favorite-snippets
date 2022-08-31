from enum import Enum
from typing import Union

from decision_tree.example.entities import (
    BinaryRange,
    SessionDto,
    ValidationDecision,
    ValidationNode,
    ValidationSwitch,
)


class IsAuthRequiredNode(ValidationNode):
    """Checks if authentication is required."""

    def _validate(self, dto: SessionDto) -> Enum:
        return BinaryRange.positive if dto.auth_required else BinaryRange.negative


class IsAuthRequiredOptionsSwitch(ValidationSwitch):
    def _get_result(
        self, dto: SessionDto, decision_option: Enum
    ) -> Union[ValidationNode, ValidationDecision]:
        if decision_option is BinaryRange.positive:
            return self._container.credential_missing_node
        elif decision_option is BinaryRange.negative:
            return self._container.is_session_valid
        raise AssertionError("Wrong enum is used, BinaryRange required")
