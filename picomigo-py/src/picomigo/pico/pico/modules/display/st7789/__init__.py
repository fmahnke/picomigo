import st7789
from machine import Pin
from pico import spi
from pico.config import config
from pico.logger import log

_config = config.st7789_display


def display():
    # global _display

    return _display


def init() -> None:
    global _display

    display_spi = spi.init(1)

    log.debug(display_spi)

    _display = st7789.ST7789(
        display_spi,
        240,
        320,
        reset=Pin(_config.reset, Pin.OUT),
        dc=Pin(_config.dc, Pin.OUT),
        cs=Pin(_config.cs, Pin.OUT),
        rotation=0
    )

    log.debug(_display)
