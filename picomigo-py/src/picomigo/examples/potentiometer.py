from time import sleep

from pico.modules import switches

switches.init()

while True:
    val = switches.pot_0.read_u16()

    print(f'Pot value: {val}')

    sleep(0.1)
