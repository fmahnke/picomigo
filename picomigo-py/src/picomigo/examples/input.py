import asyncio
from typing import Any

import pico
import vga2_16x32 as font
from pico.modules import display as display_module
from pico.modules import input
from pico.modules.events import signal
from pico.modules.input import RotaryEncoderEvent, encoder

_button_on = signal('button_on')
_button_off = signal('button_off')


class InputExample:
    _line_height: int = 34
    _last_event: str | None
    _display: Any
    _count: int = 0

    def __init__(self) -> None:
        self._last_event = None

        encoder.on(RotaryEncoderEvent.CLICK, self._click_event_listener)
        encoder.on(RotaryEncoderEvent.TURN_LEFT, self._turn_left_listener)
        encoder.on(
            RotaryEncoderEvent.TURN_LEFT_FAST, self._turn_left_fast_listener
        )
        encoder.on(RotaryEncoderEvent.TURN_RIGHT, self._turn_right_listener)
        encoder.on(
            RotaryEncoderEvent.TURN_RIGHT_FAST, self._turn_right_fast_listener
        )

        self._display = display_module.display()

        self._display.init()

        self._display.rotation(3)

        self._display.fill(0)

    def _click_event_listener(self):
        self._last_event = 'click'

    def _turn_left_listener(self):
        self._last_event = 'left'

    def _turn_left_fast_listener(self):
        self._last_event = 'left ! '

    def _turn_right_listener(self):
        self._last_event = 'right'

    def _turn_right_fast_listener(self):
        self._last_event = 'right !'

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

        message = f'Encoder: {self._last_event}'

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
