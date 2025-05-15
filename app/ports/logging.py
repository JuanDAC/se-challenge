from abc import ABC, abstractmethod


class LoggerServicePort(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str, exc_info: bool = False):
        pass

    @abstractmethod
    def warning(self, message: str):
        pass
