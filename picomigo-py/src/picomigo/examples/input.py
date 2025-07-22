import asyncio

import pico
import vga2_16x32 as font
from pico.modules import display as display_module
from pico.modules import input
from pico.modules.input import RotaryEncoderEvent, encoder


class InputExample:
    _line_height: int = 34
    _last_event: str | None

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

    async def main(self):
        display = display_module.display()

        display.init()

        display.rotation(3)
        display.fill(0)

        count = 0

        while True:

            print(f'--- {count}')

            count += 1

            y = 0

            for it in ['button_0', 'button_1']:
                if input.is_on(it):
                    state = 'on'
                else:
                    state = 'off'

                message = f'Switch {it[-1]} is: {state}'
                print(message)

                display.text(font, message, 0, y)

                y += self._line_height

            message = f'Encoder: {self._last_event}'

            print(message)

            display.text(font, message, 0, y)

            await asyncio.sleep(1)


example = InputExample()

pico.run(example.main)
