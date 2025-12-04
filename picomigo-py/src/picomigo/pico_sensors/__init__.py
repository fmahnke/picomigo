# import asyncio

# import pico

# async def main():
#     mcp = i2c.expander_0

#     output = 0

#     while True:
#         if output == 8:
#             output = 0

#         mcp.porta.gpio = 0

#         mcp[output].output(1)

#         output += 1

#         await asyncio.sleep(0.5)

#         # # list interface
#         # mcp[0].input()
#         # mcp[1].input(pull=1)
#         # mcp[1].value()
#         # mcp[2].output(1)
#         # mcp[3].output(0)

#         # await asyncio.sleep(1.0)
#         # # method interface
#         # mcp.pin(0, mode=1)
#         # mcp.pin(1, mode=1, pullup=True)
#         # mcp.pin(1)
#         # mcp.pin(2, mode=0, value=1)
#         # mcp.pin(3, mode=0, value=0)

#         # await asyncio.sleep(1.0)

#         # mcp.config(interrupt_polarity=0, interrupt_mirror=1)

#         # # property interface 16-bit
#         # mcp.mode = 0xfffe
#         # mcp.gpio = 0x0001

#         # # property interface 8-bit
#         # mcp.porta.mode = 0xfe
#         # mcp.portb.mode = 0xff
#         # mcp.porta.gpio = 0x01
#         # mcp.portb.gpio = 0x02

#         # await asyncio.sleep(1.0)

import machine
import pico
# pico.run(main)
import uasyncio as asyncio
from machine import Pin
from mcp23017 import MCP23017
from pico import i2c
from pico.comms import LocalPeer
from pico.logger import log
from pico.modules import input
from pico.modules.events import signal
from vl53l0x import VL53L0X

_button_on = signal('button_on')
_button_off = signal('button_off')

_encoder_click = signal('encoder_click')
_encoder_multiple_click = signal('encoder_multiple_click')
_encoder_any = signal('encoder_any')
_encoder_turn_left = signal('encoder_turn_left')
_encoder_turn_left_fast = signal('encoder_turn_left_fast')
_encoder_turn_right = signal('encoder_turn_right')
_encoder_turn_right_fast = signal('encoder_turn_right_fast')


class PicoSensors:
    class LM393:
        _out_pin: Pin

        def __init__(self, out_pin: int) -> None:
            self._out_pin = Pin(out_pin, mode=Pin.IN)

        def value(self) -> int:
            return self._out_pin.value()

    _last_event: str | None
    _count: int = 0
    _mcp: MCP23017 | None
    _comms: LocalPeer
    _loop_sleep_ms: int
    _i2c_0: machine.I2C
    _vl53: VL53L0X
    _lm393: LM393

    def __init__(self) -> None:
        self._i2c_0 = machine.I2C(0, scl=5, sda=4, freq=400000)

        self._vl53 = VL53L0X(self._i2c_0)
        self._vl53.measurement_timing_budget = 200000  # microseconds

        self._lm393 = PicoSensors.LM393(3)

        self._comms = LocalPeer()

        self._mcp = None

        self._last_event = None
        self._rotation: int = 0
        self._need_update: bool = True

        self._loop_sleep_ms = 0

        _ = _encoder_click.connect(self._click_event_listener)
        _ = _encoder_turn_left.connect(self._turn_left_listener)
        _ = _encoder_turn_left_fast.connect(self._turn_left_fast_listener)
        _ = _encoder_turn_right.connect(self._turn_right_listener)
        _ = _encoder_turn_right_fast.connect(self._turn_right_fast_listener)

    def _click_event_listener(self, _: object):
        self._last_event = 'click'

        self._need_update = True

        self._comms.send('encoder event')

    def _turn_left_listener(self, _: object):
        log.debug('turn left')

        self._last_event = 'left'
        self._rotation -= 1

        self._need_update = True

        self._comms.send('encoder left')

    def _turn_left_fast_listener(self, _: object):
        log.debug('turn left fast')

        self._last_event = 'left ! '

        self._need_update = True

        self._comms.send('encoder ERROR')

    def _turn_right_listener(self, _: object):
        log.debug('turn right')

        self._last_event = 'right'
        self._rotation += 1

        self._need_update = True

        self._comms.send('encoder right')

    def _turn_right_fast_listener(self, _: object):
        log.debug('turn right fast')

        self._last_event = 'right !'

        self._need_update = True

        self._comms.send('encoder ERROR')

    def _print_status(self) -> None:
        # print(f'--- {self._count}')

        self._count += 1

        for it in ['button_0', 'button_1']:
            if input.is_on(it):
                state = 'on'
            else:
                state = 'off'

            message = f'Switch {it[-1]} is: {state}'
            # print(message)

        message = f'Encoder: {self._last_event} ({self._rotation})'

        # print(message)

    async def main_events(self):
        self._mcp = i2c.expander_0

        self._vl53.start_continuous()

        def button_on(button: str) -> None:
            # print(f'button on: {button}')

            self._print_status()

        def button_off(button: str) -> None:
            # print(f'button off: {button}')

            self._print_status()

        _ = _button_on.connect(button_on)
        _ = _button_off.connect(button_off)

        while True:
            # if output == 8:
            #     output = 0

            # self._mcp.porta.gpio = 0

            # self._mcp[output].output(1)

            # output += 1

            if self._need_update:
                # self._print_status()

                self._need_update = False

            distance = self._vl53.range

            if not isinstance(distance, int):
                self._comms.send(f'distance error type={type(distance)}')
            else:
                self._comms.send(f'distance {distance}')

            # lm393 = self._lm393.value()

            # self._comms.send(f'lm393 {lm393}')

            await asyncio.sleep_ms(self._loop_sleep_ms)

    # async def main(self):
    #     self._mcp = i2c.expander_0

    #     output = 0

    #     while True:
    #         print(f'--- {self._count}')

    #         if output == 8:
    #             output = 0

    #         self._mcp.porta.gpio = 0

    #         self._mcp[output
    #                   ].output(  # pyright: ignore[reportUnknownMemberType]
    #                       1
    #                   )

    #         output += 1

    #         message = f'Encoder: {self._last_event}'

    #         print(message)

    #         await asyncio.sleep(1)


example = PicoSensors()

pico.run(example.main_events)
