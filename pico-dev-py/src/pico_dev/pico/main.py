from time import sleep

import utime
from machine import Pin
from pico.modules import switches

_pin_5 = Pin(5, Pin.OUT)

switches.init()

_pin_5.value(1)

while True:
    switches._encoder.raw_tick()  # handle encoder events
    utime.sleep_ms(1)  # delay'''

    val = switches.pot_0.read_u16()

    print(f'Pot value: {val}')
'''
count = 0

while True:
    print(f'--- {count}')

    count += 1

    for it in ['rotary encoder', 'button_0', 'button_1']:
        if switches.is_on(it):
            state = 'on'
        else:
            state = 'off'

        print(f'Switch {it} is: {state}')

        encoder_value = switches._encoder.value()

        print(f'Encoder: {encoder_value}')

    sleep(1.0)
'''
