import asyncio

from pico.modules.input import rotary_encoder, switches
from pico.config import Config

from .rotary_encoder import RotaryEncoderEvent
from .switches import is_on, pot_0

__all__ = [
    'RotaryEncoderEvent',
    'init',
    'is_on',
    'pot_0',
    'switches',
    'tick',
]


def init(config: Config | None = None) -> None:
    rotary_encoder.init(config)

    switches.init(config)


async def tick() -> None:
    _ = await asyncio.gather(
        rotary_encoder.async_tick(1),
        switches.tick(),
    )
