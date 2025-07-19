from time import sleep

from pico.modules import switches

switches.init()

while True:
    print('pico-dev ready...')

    sleep(5)
