"""Basic architecture for a decision tree with cycles and variable amount of child nodes."""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, Union


class BaseDto:
    """Data transfer object that keeps all dynamic data for decision purposes."""


class Decision:
    """Any king of final decision in the end of the algorythm."""


class AbstractNode(metaclass=ABCMeta):
    """Base decision tree node interface."""

    @abstractmethod
    def decide(self, data_iterator: BaseDto) -> Union[AbstractNode, Decision]:
        """Returns next node or final decision."""


class SwitchedNode(AbstractNode, metaclass=ABCMeta):
    """Base node with attached Switch instance."""

    def __init__(self, decision_switch: DecisionSwitch):
        self._decision_switch = decision_switch

    def decide(self, dto: BaseDto) -> Union[AbstractNode, Decision]:
        """Returns next node or final decision."""
        return self._decision_switch.get_result(dto, self._decide(dto))

    @abstractmethod
    def _decide(self, dto: BaseDto) -> Enum:
        raise NotImplementedError


class AbstractTreeContainer:
    """Nodes container with calculation."""

    _initial_node: AbstractNode = NotImplemented

    def calculate(self, dto: BaseDto) -> Decision:
        """Calculates the result."""
        current_node = self._initial_node
        while True:
            local_decision = current_node.decide(dto)
            if isinstance(local_decision, AbstractNode):
                current_node = local_decision
            elif isinstance(local_decision, Decision):
                return local_decision
            else:
                raise AttributeError(
                    f"Unexpected decision result: {local_decision.__class__.__name__}",
                )


T = TypeVar("T", bound=AbstractTreeContainer)


class DecisionSwitch(Generic[T], metaclass=ABCMeta):
    """An entity that matches node decision with results."""

    def __init__(self, container: T):
        self._container = container

    @abstractmethod
    def get_result(
        self, dto: BaseDto, decision_option: Enum
    ) -> Union[AbstractNode, Decision]:
        """Interprets decision option."""
        raise NotImplementedError
