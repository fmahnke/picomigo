# pyright: reportDeprecated=false

import asyncio
from math import ceil
from os import statvfs
# from collections.abc import Coroutine
from typing import Callable, Coroutine

import vga2_16x32 as font
from machine import ADC
from pico.modules import display as display_module
from pico.modules import input

_temp_sensor = ADC(4)


def run(callback: Callable[..., Coroutine[None, None, None]]) -> None:
    asyncio.run(_async_run(callback))


def display():
    return display_module.display


async def _show_temp():
    _display = display_module.display()

    while True:
        y = 34 * 6

        voltage = _temp_sensor.read_u16() * (3.3 / 65535.0)
        temp_c = 27 - (voltage - 0.706) / 0.001721

        vfs = statvfs('/')

        free = f'{round(vfs[3] / vfs[2] * 100)}%'

        _display.text(font, f'{ceil(temp_c)} C | {free}', 0, y)

        await asyncio.sleep(5)


async def _async_run(
    callback: Callable[..., Coroutine[None, None, None]]
) -> None:
    _ = await asyncio.gather(
        input.tick(),
        callback(),
        _show_temp(),
    )


def _init() -> None:
    input.init()
    display_module.init()


_init()
