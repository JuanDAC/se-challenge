import inspect
from abc import ABC, abstractmethod
from typing import List

from app.ports.transactional.transaction_manager import TransactionManagerPort
from app.ports.transactional.transactionable import Transactionable


class NotDefinedTransactionManagerError(Exception):
    """
    Raised when transaction manager is not set
    """

    pass


class AtomClass(ABC):
    """
    Description:
    Atom use cases port class

    Methods:
    - execute() -> None : Execute atom
    """

    transaction_manager: TransactionManagerPort = None

    post_transactions: List

    @abstractmethod
    def execute(self) -> None:
        pass

    def after_transaction_execute(self, callback: callable):
        if not hasattr(self, "post_transactions"):
            self.post_transactions = []

        self.post_transactions.append(callback)


class Atom:
    @staticmethod
    def on_class(cls):
        original_execute = cls.execute

        def execute(self) -> None:
            if self.transaction_manager is None:
                raise NotDefinedTransactionManagerError(
                    f"Transaction manager is not set on {self.__class__.__name__}"
                )

            result = None
            with self.transaction_manager.get_transaction_context() as session:
                Atom._set_transaction_context_for_attrs(self, session)
                result = original_execute(self)

                post_transaction = getattr(self, "post_transactions", [])
                if len(post_transaction) > 0:
                    session.commit()
                    for callback in post_transaction:
                        callback()

                Atom._clear_transaction_context_for_attrs(self)

            self.post_transactions = []
            self.pre_transactions = []

            return result

        cls.execute = execute
        return cls

    @staticmethod
    def _set_transaction_context_for_attrs(instance, session):
        for attr_name, attr_value in inspect.getmembers(instance):
            if Atom._is_transactionable_attr(attr_name, attr_value):
                attr_value.set_transaction_context(session)

    @staticmethod
    def _clear_transaction_context_for_attrs(instance):
        for attr_name, attr_value in inspect.getmembers(instance):
            if Atom._is_transactionable_attr(attr_name, attr_value):
                attr_value.set_transaction_context(None)

    @staticmethod
    def _is_transactionable_attr(attr_name, attr_value):
        return (
            not attr_name.startswith("__")
            and not inspect.ismethod(attr_value)
            and isinstance(attr_value, Transactionable)
        )
