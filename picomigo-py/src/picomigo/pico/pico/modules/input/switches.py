# pyright: reportArgumentType=false,reportIndexIssue=false
# pyright: reportUnknownMemberType=false,reportUnknownVariableType=false

import asyncio

from machine import ADC, Pin
from pico.config import switches as config
from pico.modules.events import signal

from .rotary_encoder import RotaryEncoderEvent, encoder

__all__ = [
    'RotaryEncoderEvent',
    'encoder',
    'init',
    'is_on',
    'pot_0',
    'switches',
    'tick'
]


class SwitchState:
    NONE: int = -1
    OFF: int = 0
    ON: int = 1


class Switch:
    def __init__(self, pin: Pin) -> None:
        self.pin: Pin = pin
        self.state: int = SwitchState.NONE


_button_on = signal('button_on')
_button_off = signal('button_off')

_button_0_on = signal('button_0_on')
_button_0_off = signal('button_0_off')
_button_1_on = signal('button_1_on')
_button_1_off = signal('button_1_off')

# def push_button_on(name: str, callback) -> None:
#     pass

pot_0 = ADC(config['potentiometer_0'])

switches: dict[str, Switch] = {}


def init() -> None:
    switches['button_0'] = Switch(Pin(config['button_0'], Pin.IN))
    switches['button_1'] = Switch(Pin(config['button_1'], Pin.IN))


async def tick() -> None:
    _ = await asyncio.gather(
        encoder.async_tick(1),
        _switches_tick(),
    )


def is_on(switch: str) -> bool:
    return switches[switch].pin.value() == 1


async def _switches_tick() -> None:
    while True:
        for k, v in switches.items():
            state = v.pin.value()

            if state != v.state:
                if state == SwitchState.OFF:
                    _ = _button_off.send(k)
                elif state == SwitchState.ON:
                    _ = _button_on.send(k)
                else:
                    raise NotImplementedError

                v.state = state

        await asyncio.sleep(0.1)
