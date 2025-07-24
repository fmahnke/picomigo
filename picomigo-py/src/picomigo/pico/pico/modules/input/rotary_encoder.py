# pyright: reportIndexIssue=false

from machine import Pin
from pico.config import switches as config
from rotary_encoder import RotaryEncoderEvent, RotaryEncoderRP2

__all__ = [
    'RotaryEncoderEvent',
    'encoder',
]

_encoder_pin_clk = Pin(config['rotary_encoder']['clk'], Pin.IN, Pin.PULL_UP)
_encoder_pin_dt = Pin(config['rotary_encoder']['dt'], Pin.IN, Pin.PULL_UP)
_encoder_pin_sw = Pin(config['rotary_encoder']['sw'], Pin.IN, Pin.PULL_UP)

encoder = RotaryEncoderRP2(_encoder_pin_clk, _encoder_pin_dt, _encoder_pin_sw)
