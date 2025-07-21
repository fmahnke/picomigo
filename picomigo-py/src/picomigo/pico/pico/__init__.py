# pyright: reportDeprecated=false

import asyncio
# from collections.abc import Coroutine
from typing import Callable, Coroutine

from pico.modules import display as display_module
from pico.modules import switches


def run(callback: Callable[..., Coroutine[None, None, None]]) -> None:
    asyncio.run(_async_run(callback))


def display():
    return display_module.display


async def _async_run(
    callback: Callable[..., Coroutine[None, None, None]]
) -> None:
    switches.init()
    display_module.init()

    _ = await asyncio.gather(
        switches.tick(),
        callback(),
    )
