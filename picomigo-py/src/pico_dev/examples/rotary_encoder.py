import asyncio

import pico


async def main():
    while True:
        await asyncio.sleep(1)


pico.run(main)
