import asyncio
from typing import Any

import pico
import vga2_16x32 as font
from pico.logger import log
from pico.modules import display as display_module
from pico.modules import input
from pico.modules.events import signal

_button_on = signal('button_on')
_button_off = signal('button_off')

_encoder_click = signal('encoder_click')
_encoder_multiple_click = signal('encoder_multiple_click')
_encoder_any = signal('encoder_any')
_encoder_turn_left = signal('encoder_turn_left')
_encoder_turn_left_fast = signal('encoder_turn_left_fast')
_encoder_turn_right = signal('encoder_turn_right')
_encoder_turn_right_fast = signal('encoder_turn_right_fast')


class InputExample:
    _line_height: int = 34
    _last_event: str | None
    _display: Any
    _count: int = 0

    def __init__(self) -> None:
        self._last_event = None
        self._rotation: int = 0
        self._need_update: bool = True

        _ = _encoder_click.connect(self._click_event_listener)
        _ = _encoder_turn_left.connect(self._turn_left_listener)
        _ = _encoder_turn_left_fast.connect(self._turn_left_fast_listener)
        _ = _encoder_turn_right.connect(self._turn_right_listener)
        _ = _encoder_turn_right_fast.connect(self._turn_right_fast_listener)

        self._display = display_module.display()

        self._display.init()

        self._display.rotation(3)

    def _click_event_listener(self, _: object):
        self._last_event = 'click'

        self._need_update = True

    def _turn_left_listener(self, _: object):
        log.debug('turn left')

        self._last_event = 'left'
        self._rotation -= 1

        self._need_update = True

    def _turn_left_fast_listener(self, _: object):
        log.debug('turn left fast')

        self._last_event = 'left ! '

        self._need_update = True

    def _turn_right_listener(self, _: object):
        log.debug('turn right')

        self._last_event = 'right'
        self._rotation += 1

        self._need_update = True

    def _turn_right_fast_listener(self, _: object):
        log.debug('turn right fast')

        self._last_event = 'right !'

        self._need_update = True

    def _print_status(self) -> None:
        print(f'--- {self._count}')

        self._count += 1

        y = 0

        for it in ['button_0', 'button_1']:
            if input.is_on(it):
                state = 'on'
            else:
                state = 'off'

            message = f'Switch {it[-1]} is: {state}'
            print(message)

            self._display.text(font, message, 0, y)

            y += self._line_height

        message = f'Encoder: {self._last_event} ({self._rotation})'

        print(message)

        self._display.text(font, message, 0, y)

    async def main_events(self):
        def button_on(button: str) -> None:
            print(f'button on: {button}')

            self._print_status()

        def button_off(button: str) -> None:
            print(f'button off: {button}')

            self._print_status()

        _ = _button_on.connect(button_on)
        _ = _button_off.connect(button_off)

        while True:
            if self._need_update:
                self._print_status()

                self._need_update = False

            await asyncio.sleep(1)

    async def main(self):
        while True:
            print(f'--- {self._count}')

            y = 0

            for it in ['button_0', 'button_1']:
                if input.is_on(it):
                    state = 'on'
                else:
                    state = 'off'

                message = f'Switch {it[-1]} is: {state}'
                print(message)

                self._display.text(font, message, 0, y)

                y += self._line_height

            message = f'Encoder: {self._last_event}'

            print(message)

            self._display.text(font, message, 0, y)

            await asyncio.sleep(1)


example = InputExample()

pico.run(example.main_events)
