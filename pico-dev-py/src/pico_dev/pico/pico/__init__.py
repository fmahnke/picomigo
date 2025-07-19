import asyncio
# from collections.abc import Coroutine
from typing import Callable, Coroutine

from pico.modules import switches


def run(callback: Callable[..., Coroutine[None, None, None]]) -> None:
    asyncio.run(_async_run(callback))


async def _async_run(
    callback: Callable[..., Coroutine[None, None, None]]
) -> None:
    await switches.init()

    while True:
        _ = await asyncio.gather(
            asyncio.create_task(switches.tick()),
            asyncio.create_task(callback()),
        )
