# pyright: reportIndexIssue=false

from typing import Any

from machine import Pin
from pico.config import Config
from pico.config import config as default_config
from pico.modules.events import signal
from rotary_encoder import RotaryEncoderEvent, RotaryEncoderRP2

__all__ = [
    'RotaryEncoderEvent',
    'encoder',
]


def _click_event_listener() -> None:
    _ = _click.send()


def _multiple_click_event_listener(count: int) -> None:
    _ = _multiple_click.send(count)


def _any_event_listener(event: RotaryEncoderEvent, click_count: int) -> None:
    _ = _any.send({'event': event, 'click_count': click_count})


def _turn_left_event_listener() -> None:
    _ = _turn_left.send()


def _turn_left_fast_event_listener() -> None:
    _ = _turn_left_fast.send()


def _turn_right_event_listener() -> None:
    _ = _turn_right.send()


def _turn_right_fast_event_listener() -> None:
    _ = _turn_right_fast.send()


class RotaryEncoder(RotaryEncoderRP2):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.on(RotaryEncoderEvent.CLICK, _click_event_listener)

        self.on(
            RotaryEncoderEvent.MULTIPLE_CLICK, _multiple_click_event_listener
        )

        self.on(RotaryEncoderEvent.ANY, _any_event_listener)

        self.on(RotaryEncoderEvent.TURN_LEFT, _turn_left_event_listener)

        self.on(
            RotaryEncoderEvent.TURN_LEFT_FAST, _turn_left_fast_event_listener
        )

        self.on(RotaryEncoderEvent.TURN_RIGHT, _turn_right_event_listener)

        self.on(
            RotaryEncoderEvent.TURN_RIGHT_FAST,
            _turn_right_fast_event_listener
        )


encoder: RotaryEncoder | None = None

_click = signal('encoder_click')
_multiple_click = signal('encoder_multiple_click')
_any = signal('encoder_any')
_turn_left = signal('encoder_turn_left')
_turn_left_fast = signal('encoder_turn_left_fast')
_turn_right = signal('encoder_turn_right')
_turn_right_fast = signal('encoder_turn_right_fast')


def init(config: Config | None = None) -> None:
    global encoder

    if config is None:
        config = default_config

    encoder_config = config.switches.rotary_encoder

    encoder_pin_clk = Pin(encoder_config.clk, Pin.IN, Pin.PULL_UP)
    encoder_pin_dt = Pin(encoder_config.dt, Pin.IN, Pin.PULL_UP)
    encoder_pin_sw = Pin(encoder_config.sw, Pin.IN, Pin.PULL_UP)

    encoder = RotaryEncoder(encoder_pin_clk, encoder_pin_dt, encoder_pin_sw)


async def async_tick(timeout: int = 1):
    global encoder

    assert encoder is not None

    await encoder.async_tick(timeout)
