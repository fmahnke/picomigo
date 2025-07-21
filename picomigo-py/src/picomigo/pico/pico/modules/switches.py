# pyright: reportArgumentType=false,reportIndexIssue=false
# pyright: reportUnknownMemberType=false,reportUnknownVariableType=false

# from dataclasses import dataclass
# from enum import Enum, auto

from typing import Any

from machine import ADC, Pin
from pico.config import switches as config
from rotary_encoder import RotaryEncoderEvent, RotaryEncoderRP2

__all__ = ['RotaryEncoderEvent', 'init', 'is_on', 'pot_0', 'switches']

# @dataclass
# class Switch:
#     name: str
#     input_pin: Pin
#     closed: bool = False
#
#
# #_switches = [
# #    Switch('rotary encoder', 17),
# #    Switch('button 0', 14),
# #    Switch('button 1', 13),
# #]
#
#
#
# class Switch1(Enum):
#     ROTARY_ENCODER = auto()
#     BUTTON_0 = auto()
#     BUTTON_1 = auto()

pot_0 = ADC(config['potentiometer_0'])

switches = {}

_encoder_pin_clk = Pin(config['rotary_encoder']['clk'], Pin.IN, Pin.PULL_UP)
_encoder_pin_dt = Pin(config['rotary_encoder']['dt'], Pin.IN, Pin.PULL_UP)
_encoder_pin_sw = Pin(config['rotary_encoder']['sw'], Pin.IN, Pin.PULL_UP)

encoder = RotaryEncoderRP2(_encoder_pin_clk, _encoder_pin_dt, _encoder_pin_sw)


# Listeners
def any_event_listener(event: Any, clicks: int):
    print(f"ANY Event ID: {event} Clicks: {clicks}")


def turn_left_listener():
    print("Turn Left")


def turn_left_fast_listener():
    print("Turn Left Fast")


def turn_right_listener():
    print("Turn Right")


def turn_right_fast_listener():
    print("Turn Right Fast")


# subscribe to events
encoder.on(RotaryEncoderEvent.ANY, any_event_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT, turn_left_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST, turn_left_fast_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT, turn_right_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST, turn_right_fast_listener)
'''
def on_click():
    print("CLICK")


def on_multy_clicks(clicks: int):
    print(f"CLICK {clicks} times")


def on_any(event_id: int, clicks: int):
    print(f"ANY {event_id}, clicks {clicks}")


encoder.on(RotaryEncoderEvent.CLICK, on_click)
encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, on_multy_clicks)
encoder.on(RotaryEncoderEvent.ANY, on_any)
'''


def init() -> None:
    # switches['rotary encoder'] = Pin(17, Pin.IN)
    switches['button_0'] = Pin(config['button_0'], Pin.IN)
    switches['button_1'] = Pin(config['button_1'], Pin.IN)


async def tick() -> None:
    await encoder.async_tick(1)


def is_on(switch: str) -> bool:
    return switches[switch].value() == 1
