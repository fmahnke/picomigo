import pico
from pico.comms import Comms


async def main():
    comms = Comms()

    await comms.read_frames()


pico.run(main)
