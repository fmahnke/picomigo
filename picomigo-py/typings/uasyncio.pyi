from typing import Any, Awaitable, Callable

async def sleep_ms(delay: int) -> None:
    ...


def run(
    main: Awaitable[Any],
    *,
    debug: None = None,
    loop_factory: None = None
) -> None:
    ...
