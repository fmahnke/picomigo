import asyncio
from typing import Any

import pico
import vga2_16x32 as font
from neopixel2 import Neopixel, slice_maker
from pico.logger import log
from pico.modules import display as display_module

_display = display_module.display()
_line_height: int = 34


# from pico.config import led as config
async def main():
    _display.init()

    _display.rotation(3)

    pixels = Neopixel(8, 0, 20, "GRB")

    print('start pixels')

    end = 8

    y = _line_height * 2
    x = 60

    _display.text(font, 'picomigo 0.1', x, y)

    while True:
        pixels.fill((0, 0, 0))
        pixels.show()

        await asyncio.sleep(1.0)

        for index in range(0, end):
            start = (0, 2, 0)
            stop = (0, 50, 0)

            pixels.set_pixel_line_gradient(0, end - 1, start, stop)

            print(f'index {index}')
            if index < end - 1:
                pixels.set_pixel(
                    slice_maker[
                        index
                        + 1:end],  # pyright: ignore[reportUnknownArgumentType]
                    (0, 0, 0)
                )

            pixels.show()

            await asyncio.sleep(0.5)


pico.run(main)
