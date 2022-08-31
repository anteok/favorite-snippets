from __future__ import annotations

from decision_tree.base import AbstractTreeContainer
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
