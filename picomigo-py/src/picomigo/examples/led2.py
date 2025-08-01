import asyncio

import pico
from neopixel2 import Neopixel, slice_maker


# from pico.config import led as config
async def main():
    pixels = Neopixel(8, 0, 20, "GRB")

    print('start pixels')

    end = 8

    while True:
        pixels.fill((0, 0, 0))
        pixels.show()

        await asyncio.sleep(1.0)

        for index in range(0, end):
            start = (0, 2, 0)
            stop = (0, 50, 0)

            pixels.set_pixel_line_gradient(0, end - 1, start, stop)

            print(f'index {index}')
            if index < end - 1:
                pixels.set_pixel(
                    slice_maker[
                        index
                        + 1:end],  # pyright: ignore[reportUnknownArgumentType]
                    (0, 0, 0)
                )

            pixels.show()

            await asyncio.sleep(0.5)


pico.run(main)
# while True:
#     pixels.set_pixel(0, (20, 0, 0))
#     pixels.show()
#
#     sleep(1.0)
#
#     pixels.set_pixel(1, (0, 20, 0))
#     pixels.show()
#
#     sleep(1.0)
#
#     pixels.set_pixel(2, (0, 0, 20))
#     pixels.show()
#
#     sleep(1.0)
#
#     pixels.set_pixel_line(0, 3, (0, 0, 0))
#     pixels.show()
#
#     sleep(1.0)
#
# pixels.set_pixel_line(5, 7, (0, 255, 0))
# pixels.show()
#
# sleep(1.0)
#
# pixels.fill((20, 5, 0))
# pixels.show()
#
# sleep(1.0)
#
# # rgbw1 = (0, 0, 50, 0)
# # rgbw2 = (50, 0, 0, 250)
# # pixels.set_pixel(42, (0, 50, 0, 0))
# # pixels.set_pixel_line(5, 7, rgbw1)
# # pixels.set_pixel_line_gradient(0, 13, rgbw1, rgbw2)
#
# print('done')
