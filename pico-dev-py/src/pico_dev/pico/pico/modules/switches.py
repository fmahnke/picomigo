# from dataclasses import dataclass
# from enum import Enum, auto

from machine import Pin

# from pico import rotary_encoder

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


def init() -> None:
    switches['rotary encoder'] = Pin(17, Pin.IN)
    switches['button_0'] = Pin(14, Pin.IN)
    switches['button_1'] = Pin(13, Pin.IN)


def is_on(switch: str) -> bool:
    return switches[switch].value() == 1
