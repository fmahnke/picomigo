import pico
from pico.comms import LocalPeer


async def main():
    comms = LocalPeer()

    await comms.read_frames()


pico.run(main)
