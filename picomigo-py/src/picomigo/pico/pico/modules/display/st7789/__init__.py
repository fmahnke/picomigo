import random

import st7789py as st7789
import vga2_16x32 as font
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


def box_lines():
    while True:
        color = st7789.color565(
            random.getrandbits(8),
            random.getrandbits(8),
            random.getrandbits(8)
        )

        _display.line(
            random.randint(0, _display.width),
            random.randint(0, _display.height),
            random.randint(0, _display.width),
            random.randint(0, _display.height),
            color,
        )

        width = random.randint(0, _display.width // 2)
        height = random.randint(0, _display.height // 2)
        col = random.randint(0, _display.width - width)
        row = random.randint(0, _display.height - height)

        _display.fill_rect(
            col,
            row,
            width,
            height,
            st7789.color565(
                random.getrandbits(8),
                random.getrandbits(8),
                random.getrandbits(8)
            ),
        )


def hello():
    """

    The big show!

    """

    while True:
        print('loop')

        for rotation in range(4):
            print(f'rotation={rotation}')

            _display.rotation(rotation)
            _display.fill(0)
            col_max = _display.width - font.WIDTH * 5
            row_max = _display.height - font.HEIGHT

            if col_max < 0 or row_max < 0:
                raise RuntimeError(
                    "This font is too big to display on this screen."
                )

            for _ in range(100):
                _display.text(
                    font,
                    "Hello",
                    random.randint(0, col_max),
                    random.randint(0, row_max),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                )


#
'''
def main():
    """

    Runs the main loop for the bounce animation.

    """

    width, height = _display.width, _display.height
    col, row = width // 2 - alien.WIDTH // 2, height // 2 - alien.HEIGHT // 2
    xd, yd = SPEED_X, SPEED_Y
    last_col, old_row = col, row

    while True:
        last = time.ticks_ms()
        _display.fill_rect(last_col, old_row, alien.WIDTH, alien.HEIGHT, 0)
        _display.bitmap(alien, col, row)
        last_col, old_row = col, row
        col, row = col + xd, row + yd
        xd = -xd if col <= 0 or col >= width - alien.WIDTH else xd
        yd = -yd if row <= 0 or row >= height - alien.HEIGHT else yd

        if time.ticks_ms() - last < TICKS:
            time.sleep_ms(TICKS - (time.ticks_ms() - last))

'''

init()
# hello()
# box_lines()
