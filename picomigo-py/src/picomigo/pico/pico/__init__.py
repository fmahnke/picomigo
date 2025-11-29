# pyright: reportDeprecated=false
# pyright: reportImportCycles=false

import asyncio
from math import ceil
from os import statvfs
# from collections.abc import Coroutine
from typing import Callable, Coroutine

import vga2_16x32 as font
from machine import ADC
from pico.config import Config, config
from pico.logger import log
from pico.modules import display as display_module
from pico.modules import input

from . import i2c

__all__ = ['config', 'init', 'input']

_temp_sensor = ADC(4)

_config = config


def run(
    callback: Callable[..., Coroutine[None, None, None]],
    config: Config | None = None
) -> None:
    init(config)

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


def init(config: Config | None = None) -> None:
    if config is None:
        config = _config

    log.add(level=config.log.level)

    i2c.init()

    input.init(config)
    display_module.init()
