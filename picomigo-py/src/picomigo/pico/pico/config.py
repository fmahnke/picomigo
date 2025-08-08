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

    spi: dict[int, 'Config.SPI']

    def __init__(self) -> None:
        self.log = Config.Log()

        self.switches = Config.Switches()

        self.led = Config.LED()

        self.st7789_display = Config.ST7789Display()

        self.spi = {
            0: Config.SPI(id=0, sck=None, mosi=None, miso=None),
            1: Config.SPI(id=1, sck=10, mosi=11, miso=None)
        }


config = Config()
