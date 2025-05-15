from typing import TypeVar, Generic, Iterator
from abc import abstractmethod, ABC
from contextlib import contextmanager

Session = TypeVar("Session")


class TransactionExecutor(Generic[Session]):
    session: Session = None

    def set_transaction_context(self, session: Session) -> None:
        self.session = session

    @contextmanager
    def get_session(self) -> Iterator[Session]:
        if not hasattr(self, "session") and self.session is None:
            raise Exception("Session is not set")
        yield self.session
