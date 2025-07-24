# pyright: reportIndexIssue=false

from typing import Any

from machine import Pin
from pico.config import switches as config
from rotary_encoder import RotaryEncoderEvent, RotaryEncoderRP2

__all__ = [
    'RotaryEncoderEvent',
    'encoder',
]


class RotaryEncoder(RotaryEncoderRP2):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


_encoder_pin_clk = Pin(config['rotary_encoder']['clk'], Pin.IN, Pin.PULL_UP)
_encoder_pin_dt = Pin(config['rotary_encoder']['dt'], Pin.IN, Pin.PULL_UP)
_encoder_pin_sw = Pin(config['rotary_encoder']['sw'], Pin.IN, Pin.PULL_UP)

encoder = RotaryEncoder(_encoder_pin_clk, _encoder_pin_dt, _encoder_pin_sw)
