import asyncio

from pico.modules import switches


async def async_some_other_task():
    print("async_some_other_task")
    while True:
        await asyncio.sleep(1)


async def main():
    await switches.init()


asyncio.run(main())
