import asyncio

import pico
from pico import i2c


async def main():
    mcp = i2c.expander_0

    output = 0

    while True:
        if output == 8:
            output = 0

        mcp.porta.gpio = 0

        mcp[output].output(1)

        output += 1

        await asyncio.sleep(0.5)

        # # list interface
        # mcp[0].input()
        # mcp[1].input(pull=1)
        # mcp[1].value()
        # mcp[2].output(1)
        # mcp[3].output(0)

        # await asyncio.sleep(1.0)
        # # method interface
        # mcp.pin(0, mode=1)
        # mcp.pin(1, mode=1, pullup=True)
        # mcp.pin(1)
        # mcp.pin(2, mode=0, value=1)
        # mcp.pin(3, mode=0, value=0)

        # await asyncio.sleep(1.0)

        # mcp.config(interrupt_polarity=0, interrupt_mirror=1)

        # # property interface 16-bit
        # mcp.mode = 0xfffe
        # mcp.gpio = 0x0001

        # # property interface 8-bit
        # mcp.porta.mode = 0xfe
        # mcp.portb.mode = 0xff
        # mcp.porta.gpio = 0x01
        # mcp.portb.gpio = 0x02

        # await asyncio.sleep(1.0)


pico.run(main)
