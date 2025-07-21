from time import sleep

from pico.modules import input

input.init()

while True:
    val = input.pot_0.read_u16()

    print(f'Pot value: {val}')

    sleep(0.1)
