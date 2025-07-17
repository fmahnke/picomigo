import utime
from pico.modules import switches

switches.init()

while True:
    switches._encoder.raw_tick()  # handle encoder events
    utime.sleep_ms(1)  # delay
