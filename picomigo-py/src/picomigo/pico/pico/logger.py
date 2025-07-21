import sys
from typing import TextIO

import micropython_logging as logging
from micropython_logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    Logger,
)

# Initialize the global logger

__all__ = ['log', 'CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'WARNING']

_name_to_level = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}


class PicoLogger(Logger):
    def add(self, sink: TextIO = sys.stderr, level: int | str = DEBUG) -> None:
        assert sink == sys.stderr

        self._set_level(level)

    def init(self, level: int | str = DEBUG) -> None:
        self._set_level(level)

    def _set_level(self, level: int | str) -> None:
        for it in self.handlers:
            it.setLevel(_level_num(level))

        self.setLevel(_level_num(level))

    @classmethod
    def from_logger(cls, logger: Logger) -> 'PicoLogger':
        ctx = PicoLogger(logger.name)

        ctx.level = logger.level
        ctx.handlers = logger.handlers
        ctx.record = logger.record

        return ctx


def _level_num(level: int | str) -> int:
    if isinstance(level, int):
        result = level
    else:
        result = _name_to_level[level]

    return result


_root_logger = logging.getLogger('root')

log = PicoLogger.from_logger(_root_logger)

log.init()
