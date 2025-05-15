from app.ports.logging import LoggerServicePort
from datetime import datetime, timezone


class ConsoleLoggerService(LoggerServicePort):
    def info(self, message: str):
        """
        Logs an informational message to the console.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - INFO: {message}")

    def error(self, message: str, exc_info: bool = False):
        """
        Logs an error message to the console.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - ERROR: {message}")
        if exc_info:
            import traceback

            print(traceback.format_exc())

    def warning(self, message: str):
        """
        Logs a warning message to the console.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - WARNING: {message}")
