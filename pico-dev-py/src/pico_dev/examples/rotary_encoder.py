import utime
from pico.modules import switches

switches.init()

while True:
    switches.encoder.raw_tick()

    utime.sleep_ms(  # pyright: ignore[reportAttributeAccessIssue,reportUnknownMemberType] # noqa: E501
        1
    )
