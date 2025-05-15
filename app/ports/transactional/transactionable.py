import inspect
from abc import ABC
from typing import TypeVar

from typing_extensions import Generic

from app.ports.transactional.transaction_executor import TransactionExecutor

Session = TypeVar("Session")


class Transactionable(ABC, Generic[Session]):
    transactionable_session: Session

    def set_transaction_context(self, transaction_context: Session):
        self.session = transaction_context
        for attr_name, attr_value in inspect.getmembers(self):
            if not attr_name.startswith("__") and not inspect.ismethod(attr_value):
                if isinstance(attr_value, (TransactionExecutor, Transactionable)):
                    attr_value.set_transaction_context(transaction_context)
