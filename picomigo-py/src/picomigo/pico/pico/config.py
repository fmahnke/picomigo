import machine

__all__ = ['config']


class Config:
    class Log:
        level: str = 'WARNING'

    class RotaryEncoder:
        clk: int = 18
        dt: int = 17
        sw: int = 19

    class Switches:
        button_0: int = 15
        button_1: int = 14
        potentiometer_0: int = 26
        rotary_encoder: 'Config.RotaryEncoder'

        def __init__(self) -> None:
            self.rotary_encoder = Config.RotaryEncoder()

    class LED:
        data: int = 20
        pio_state_machine_id: int = 0
        led_count: int = 8

    class ST7789Display:
        reset: int = 9
        dc: int = 8
        cs: int = 0

    class I2C:
        id: int
        scl: int
        sda: int
        freq: int

        def __init__(
            self, id: int, *, scl: int, sda: int, freq: int = 400_000
        ) -> None:
            self.id = id
            self.scl = scl
            self.sda = sda
            self.freq = freq

    class I2CExpander:
        id: int = 1
        address: int = 0x20

    class SPI:
        id: int
        baudrate: int
        polarity: int
        phase: int
        bits: int
        firstbit: int
        sck: int | None
        mosi: int | None
        miso: int | None

        def __init__(
            self,
            id: int,
            baudrate: int = 1_000_000,
            *,
            polarity: int = 0,
            phase: int = 0,
            bits: int = 8,
            firstbit: int = machine.SPI.MSB,
            sck: int | None = None,
            mosi: int | None = None,
            miso: int | None = None,
        ) -> None:
            self.id = id
            self.baudrate = baudrate
            self.polarity = polarity
            self.phase = phase
            self.bits = bits
            self.firstbit = firstbit
            self.sck = sck
            self.mosi = mosi
            self.miso = miso

    log: 'Config.Log'

    switches: 'Config.Switches'

    led: 'Config.LED'

    st7789_display: 'Config.ST7789Display'

    i2c: dict[int, 'Config.I2C']

    i2c_expander: 'Config.I2CExpander'

    spi: dict[int, 'Config.SPI']

    def __init__(self) -> None:
        self.log = Config.Log()

        self.switches = Config.Switches()

        self.led = Config.LED()

        self.st7789_display = Config.ST7789Display()

        self.i2c = {
            1: Config.I2C(id=1, scl=19, sda=18),
        }

        self.i2c_expander = Config.I2CExpander()

        self.spi = {
            0: Config.SPI(id=0, sck=None, mosi=None, miso=None),
            1: Config.SPI(id=1, sck=10, mosi=11, miso=None)
        }


config = Config()
