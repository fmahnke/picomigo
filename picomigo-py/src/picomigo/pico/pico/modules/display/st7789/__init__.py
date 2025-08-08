import st7789
from machine import Pin
from pico import spi
from pico.logger import log


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
        reset=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        cs=Pin(0, Pin.OUT),
        rotation=0
    )

    log.debug(_display)
