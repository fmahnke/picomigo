from typing import Final

__all__ = [
    "CRITICAL",
    "DEBUG",
    "ERROR",
    "Formatter",
    "Handler",
    "INFO",
    "Logger",
    "NOTSET",
    "WARN",
    "WARNING",
    "log",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
]

CRITICAL: Final = 50
ERROR: Final = 40
WARNING: Final = 30
WARN: Final = WARNING
INFO: Final = 20
DEBUG: Final = 10
NOTSET: Final = 0


class LogRecord:
    def set(self, name: str, level: int, message: str) -> None: ...


class Handler:
    level: int  # undocumented
    formatter: Formatter | None  # undocumented

    def __init__(self, level: int = NOTSET) -> None: ...

    def close(self) -> None: ...

    def setLevel(self, level: int) -> None: ...

    def setFormatter(self, formatter) -> None: ...

    def format(self, record: LogRecord) -> str: ...


class Formatter:
    def __init__(self, fmt=None, datefmt=None) -> None: ...

    def usesTime(self) -> bool: ...

    def formatTime(self, datefmt, record) -> str: ...

    def format(self, record) -> str: ...


class Logger:
    name: str
    level: int
    handlers: list[Handler]
    record: LogRecord

    def __init__(self, name: str, level: int = NOTSET) -> None: ...

    def setLevel(self, level: int) -> None: ...

    def log(self, level, msg: object, *args: object) -> None: ...

    def debug(self, msg: object, *args: object) -> None: ...

    def info(self, msg: object, *args: object) -> None: ...

    def warning(self, msg: object, *args: object) -> None: ...

    def error(self, msg: object, *args: object) -> None: ...

    def critical(self, msg: object, *args: object) -> None: ...


def getLogger(name: str | None = None) -> Logger: ...
