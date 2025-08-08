from machine import I2C
from mcp23017 import MCP23017
from pico.config import config

__all__ = ['expander_0', 'i2c', 'init']

expander_0: MCP23017

i2c: dict[int, I2C] = {}


def init() -> None:
    global expander_0

    i2c_1 = _init(1)

    expander_config = config.i2c_expander

    assert expander_config.id == 1

    expander_0 = MCP23017(i2c_1, expander_config.address)


def _init(id: int) -> I2C:
    global i2c

    if id not in config.i2c:
        raise ValueError(f'invalid I2C id: {id}')

    i2c_config = config.i2c[id]

    result = I2C(i2c_config.id, scl=i2c_config.scl, sda=i2c_config.sda)

    i2c[i2c_config.id] = result

    return result
