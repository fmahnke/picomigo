from time import sleep

from pico.modules import input

input.init()

while True:
    print('picomigo ready...')

    sleep(5)
