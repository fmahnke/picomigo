import asyncio
from typing import Any

import pico
from pico.logger import log


# from pico.config import led as config
async def main():
    while True:
        await asyncio.sleep(0.5)


pico.run(main)
