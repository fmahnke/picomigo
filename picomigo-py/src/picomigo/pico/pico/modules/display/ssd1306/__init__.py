import ssd1306
from machine import I2C, Pin

_display = None


def display():
    global _display

    return _display


def init() -> None:
    global _display

    # Initialize I2C (using GP4 for SDA and GP5 for SCL)
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

    # Create the OLED display object
    oled_width = 128
    oled_height = 64
    _display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    # Clear the display at the start
    _display.fill(0)
    _display.show()
