import time

import neopixel
from machine import Pin

ws_pin = 0
led_num = 16
BRIGHTNESS = 0.2  # Adjust the brightness (0.0 - 1.0)

_bpp = 3

if _bpp == 3:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
elif _bpp == 4:
    red = (255, 0, 0, 0)
    green = (0, 255, 0, 0)
    blue = (0, 0, 255, 0)
    black = (0, 0, 0, 0)
else:
    raise NotImplementedError

neoRing = neopixel.NeoPixel(Pin(ws_pin), led_num, bpp=_bpp, timing=1)


def set_brightness(color):
    r, g, b = color
    r = int(r * BRIGHTNESS)
    g = int(g * BRIGHTNESS)
    b = int(b * BRIGHTNESS)
    return (r, g, b)


def off():
    # color = (255, 0, 0)  # Red color
    # color = set_brightness(color)
    # neoRing.fill((0, 0, 0))
    # neoRing.write()
    neoRing[0] = (255, 0, 0, 0)
    neoRing.write()


colors = [red, green, blue]


def set_color(color) -> None:
    # color = set_brightness(color)

    # for it in range(0, 3):
    #     neoRing[it] = red

    neoRing[0] = red
    neoRing[1] = green
    neoRing[2] = blue

    for it in range(3, len(neoRing)):
        neoRing[it] = black

    # neoRing.fill(color)

    neoRing.write()


def loop():
    index = 0

    while True:
        if index == len(colors):
            index = 0

        color = colors[index]

        index += 1

        print(f'set color: {color}')

        set_color(color)

        time.sleep(1)


'''
print('turn off')

while True:
    off()
    time.sleep(1)
'''

loop()
