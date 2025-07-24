# pyright: reportDeprecated=false

import asyncio
# from collections.abc import Coroutine
from typing import Callable, Coroutine

from pico.modules import display as display_module
from pico.modules import input


def run(callback: Callable[..., Coroutine[None, None, None]]) -> None:
    asyncio.run(_async_run(callback))


def display():
    return display_module.display


async def _async_run(
    callback: Callable[..., Coroutine[None, None, None]]
) -> None:
    _ = await asyncio.gather(
        input.tick(),
        callback(),
    )


def _init() -> None:
    input.init()
    display_module.init()


_init()
