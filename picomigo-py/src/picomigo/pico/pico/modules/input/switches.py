# pyright: reportArgumentType=false,reportIndexIssue=false
# pyright: reportUnknownMemberType=false,reportUnknownVariableType=false

from machine import ADC, Pin
from pico.config import switches as config
from rotary_encoder import RotaryEncoderEvent, RotaryEncoderRP2

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
    NONE: int = 0
    ON: int = 1
    OFF: int = 2


class Switch:
    def __init__(self, pin: Pin) -> None:
        self.pin: Pin = pin
        self.state: int = SwitchState.NONE


pot_0 = ADC(config['potentiometer_0'])

switches = {}

_encoder_pin_clk = Pin(config['rotary_encoder']['clk'], Pin.IN, Pin.PULL_UP)
_encoder_pin_dt = Pin(config['rotary_encoder']['dt'], Pin.IN, Pin.PULL_UP)
_encoder_pin_sw = Pin(config['rotary_encoder']['sw'], Pin.IN, Pin.PULL_UP)

encoder = RotaryEncoderRP2(_encoder_pin_clk, _encoder_pin_dt, _encoder_pin_sw)


def init() -> None:
    switches['button_0'] = Switch(Pin(config['button_0'], Pin.IN))
    switches['button_1'] = Switch(Pin(config['button_1'], Pin.IN))


async def tick() -> None:
    await encoder.async_tick(1)


def is_on(switch: str) -> bool:
    return switches[switch].pin.value() == 1
