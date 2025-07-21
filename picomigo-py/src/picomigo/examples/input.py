import asyncio

import pico
from pico.modules import input


async def main():
    count = 0

    while True:
        print(f'--- {count}')

        count += 1

        for it in ['button_0', 'button_1']:
            if input.is_on(it):
                state = 'on'
            else:
                state = 'off'

            print(f'Switch {it} is: {state}')

        await asyncio.sleep(1)


pico.run(main)
