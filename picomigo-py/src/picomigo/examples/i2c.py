import asyncio
from typing import Any

import pico
from machine import I2C, Pin
from pico.logger import log

# create I2C peripheral at frequency of 400kHz
# depending on the port, extra parameters may be required
# to select the peripheral and/or pins to use

sdaPIN = Pin(18)
sclPIN = Pin(19)
reset = Pin(22, Pin.OUT, value=1)
i2c = I2C(1, sda=sdaPIN, scl=sclPIN, freq=400000)

io_dir_a = 0x00
gpio_a = 0x12


# from pico.config import led as config
async def main():
    reset.value(1)
    # scan for peripherals, returning a list of 7-bit addresses

    log.warning('scan')

    # i2c.scan()

    # A -> output

    log.warning('A -> output')

    # i2c.writeto_mem(0x20, io_dir_a, b'\x00')
    i2c.writeto_mem(0x20, io_dir_a, bytes([0x00]))
    # i2c.writeto_mem(0x20, 0x12, b'\x00')
    '''
    i2c.writeto(42, b'123')

    # read 3 bytes from memory of peripheral 42,

    i2c.readfrom(42, 4)

    #   starting at memory-address 8 in the peripheral

    i2c.readfrom_mem(42, 8, 3)

    # write 1 byte to memory of peripheral 42
    #   starting at address 2 in the peripheral

    i2c.writeto_mem(42, 2, b'\x10')
    '''

    log.warning('A -> 0xFF')

    all = False
    output = 1

    while True:
        if all:
            # i2c.writeto(gpio_a, b'\xFF')
            # i2c.writeto(0x13, b'\xFF')
            output = 0xFF
        else:
            output <<= 1

            if output == 0x100:
                output = 1

        i2c.writeto_mem(0x20, gpio_a, bytes([output]))

        await asyncio.sleep(0.5)


pico.run(main)
