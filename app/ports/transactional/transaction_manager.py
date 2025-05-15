from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

Session = TypeVar("Session")


class TransactionManagerPort(ABC, Generic[Session]):
    @abstractmethod
    def get_transaction_context(self) -> Iterable[Session]:
        pass
