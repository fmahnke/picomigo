from machine import SPI
from pico.config import config


def init(id: int) -> SPI:
    if id not in config.spi:
        raise ValueError(f'invalid SPI id: {id}')

    spi_config = config.spi[id]

    result = SPI(
        spi_config.id,
        spi_config.baudrate,
        polarity=spi_config.polarity,
        phase=spi_config.phase,
        bits=spi_config.bits,
        firstbit=spi_config.firstbit,
        sck=spi_config.sck,
        mosi=spi_config.mosi,
        miso=spi_config.miso
    )

    return result
