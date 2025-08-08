# import asyncio
import time

import pico
from machine import ADC, PWM, Pin

_tone_min = 100
_tone_max = 750
_moisture_threshold_min = 45000
_moisture_threshold_max = 65535
_tone_range = _moisture_threshold_max - _moisture_threshold_min


class MoistureExample:
    _input: ADC = ADC(26)
    _buzzer: PWM = PWM(Pin(22))
    _duty: int = int(5000)
    _tone: bool = True
    _step: int = 0
    _next_update: int = 0

    async def run(self):
        while True:
            now = time.time_ns()

            moisture = self._input.read_u16()

            # print(f'moisture: {moisture}')

            if moisture < _moisture_threshold_min:
                silent = True
            else:
                silent = False

            freq = int(
                _tone_min + (moisture - _moisture_threshold_min) / _tone_range
                * _tone_max
            )
            '''
            freq = int(
                _tone_min
                + (_moisture_max - moisture) / _moisture_max * _tone_max
            )
            '''

            if now > self._next_update:
                print(f'moisture: {moisture}, freq: {freq}, now: {now}')

                self._next_update = now + 100000000

            if self._tone:
                if silent:
                    _ = self._buzzer.duty_u16(0)
                else:
                    self._buzzer.freq(freq)
                    _ = self._buzzer.duty_u16(self._duty)


moisture_example = MoistureExample()

pico.run(moisture_example.run)
