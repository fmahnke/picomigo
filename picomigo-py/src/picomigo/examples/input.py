import asyncio

import pico
from pico.modules import input


async def main():
    display = pico.display()

    count = 0

    while True:
        display.fill(0)

        print(f'--- {count}')

        count += 1

        y = 0

        for it in ['button_0', 'button_1']:
            if input.is_on(it):
                state = 'on'
            else:
                state = 'off'

            message = f'Switch {it[-1]} is: {state}'
            print(message)

            display.text(message, 0, y)

            y += 10

        display.show()

        await asyncio.sleep(1)


pico.run(main)
