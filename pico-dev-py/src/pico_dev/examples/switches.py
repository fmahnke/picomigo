import asyncio
from time import sleep

import pico
from pico.modules import switches


async def main():
    await switches.init()

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


count = 0


async def main2():
    global count

    print(f'--- {count}')

    count += 1

    for it in ['button_0', 'button_1']:
        if switches.is_on(it):
            state = 'on'
        else:
            state = 'off'

        print(f'Switch {it} is: {state}')

    sleep(1.0)


print('start main')
pico.run(main2)
# asyncio.run(main())
print('done main')
