import st7789
from machine import SPI, Pin
from pico.logger import log


def display():
    # global _display

    return _display


def init() -> None:
    global _display

    spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=None)

    log.debug(spi)

    _display = st7789.ST7789(
        spi,
        240,
        320,
        reset=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        cs=Pin(0, Pin.OUT),
        rotation=0
    )

    log.debug(_display)
