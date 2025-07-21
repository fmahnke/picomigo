from time import sleep

from pico.modules import switches

switches.init()

while True:
    print('picomigo ready...')

    sleep(5)
