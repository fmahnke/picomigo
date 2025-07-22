"""
scroll.py
=========

.. figure:: ../_static/scroll.jpg
    :align: center

    Test for hardware scrolling.

Smoothly scrolls all font characters up the screen.
Only works with fonts with heights that are even multiples of the screen height,
(i.e. 8 or 16 pixels high)

.. note:: This example requires the following modules:

  .. hlist::
    :columns: 3

    - `st7789py`
    - `tft_config`
    - `vga2_bold_16x16`

"""

import st7789py as st7789
import utime
import vga2_16x32 as font
from pico.modules.display import display


def main():
    """ main """

    tft = display.display()

    last_line = tft.height - font.HEIGHT
    tfa = 0
    bfa = 0
    tft.vscrdef(tfa, 240, bfa)

    tft.fill(st7789.BLUE)
    scroll = 0
    character = 0
    col = tft.width // 2 - 5 * font.WIDTH // 2

    while True:
        tft.fill_rect(0, scroll, tft.width, 1, st7789.BLUE)

        if scroll % font.HEIGHT == 0:
            tft.text(
                font,
                f'x{character:02x} {chr(character)}',
                col, (scroll + last_line) % tft.height,
                st7789.WHITE,
                st7789.BLUE
            )

            character = character + 1 if character < 256 else 0

        tft.vscsad(scroll + tfa)
        scroll += 1

        if scroll == tft.height:
            scroll = 0

        utime.sleep(0.01)


main()
