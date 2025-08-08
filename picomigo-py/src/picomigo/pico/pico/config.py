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

    log: 'Config.Log'

    switches: 'Config.Switches'

    led: 'Config.LED'

    def __init__(self) -> None:
        self.log = Config.Log()

        self.switches = Config.Switches()

        self.led = Config.LED()


config = Config()
