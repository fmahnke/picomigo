# from dataclasses import dataclass
# from enum import Enum, auto

from machine import Pin
from pico.rotary_encoder import RotaryEncoderEvent, RotaryEncoderRP2

__all__ = ['init', 'is_on', 'switches']

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

switches = {}

_encoder_pin_clk = Pin(9, Pin.IN, Pin.PULL_UP)
_encoder_pin_dt = Pin(6, Pin.IN, Pin.PULL_UP)
_encoder_pin_sw = Pin(17, Pin.IN, Pin.PULL_UP)

_encoder = RotaryEncoderRP2(_encoder_pin_clk, _encoder_pin_dt, _encoder_pin_sw)


# Listeners
def any_event_listener(event, clicks):
    print(f"ANY Event ID: {event} Clicks: {clicks}")


def turn_left_listener():
    print(f"Turn Left")


def turn_left_fast_listener():
    print(f"Turn Left Fast")


def turn_right_listener():
    print(f"Turn Right")


def turn_right_fast_listener():
    print(f"Turn Right Fast")


# subscribe to events
_encoder.on(RotaryEncoderEvent.ANY, any_event_listener)
_encoder.on(RotaryEncoderEvent.TURN_LEFT, turn_left_listener)
_encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST, turn_left_fast_listener)
_encoder.on(RotaryEncoderEvent.TURN_RIGHT, turn_right_listener)
_encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST, turn_right_fast_listener)
'''
def on_click():
    print("CLICK")


def on_multy_clicks(clicks: int):
    print(f"CLICK {clicks} times")


def on_any(event_id: int, clicks: int):
    print(f"ANY {event_id}, clicks {clicks}")


_encoder.on(RotaryEncoderEvent.CLICK, on_click)
_encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, on_multy_clicks)
_encoder.on(RotaryEncoderEvent.ANY, on_any)
'''


def init() -> None:
    # switches['rotary encoder'] = Pin(17, Pin.IN)
    switches['button_0'] = Pin(14, Pin.IN)
    switches['button_1'] = Pin(13, Pin.IN)


def is_on(switch: str) -> bool:
    return switches[switch].value() == 1
