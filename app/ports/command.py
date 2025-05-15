from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel

Return = TypeVar("Return")
Attributes = TypeVar("Attributes", bound=BaseModel)


class Command(ABC, Generic[Return, Attributes]):
    """
    Abstract base class for commands (use cases or services that perform an action).
    Expects attributes to be set via `set_params` before calling `execute`.
    """

    params: Attributes

    @abstractmethod
    def execute(self) -> Return:
        """Executes the command with the previously set parameters."""
        pass

    def set_params(self, attributes: Attributes) -> None:
        """Sets the parameters for command execution."""
        self.params = attributes
