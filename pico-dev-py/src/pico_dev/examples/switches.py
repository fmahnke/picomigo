from time import sleep

from pico.modules import switches

switches.init()

count = 0

while True:
    print(f'--- {count}')

    count += 1

    for it in ['button_0', 'button_1']:
        if switches.is_on(it):
            state = 'on'
        else:
            state = 'off'

        print(f'Switch {it} is: {state}')

    sleep(1.0)
