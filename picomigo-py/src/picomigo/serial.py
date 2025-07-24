import sys

from mktech.serial_port import miniterm


def main() -> None:
    sys.argv = sys.argv[:-1] + ['--exit-char', '24']

    miniterm.main(default_port='/dev/ttyACM0', default_baudrate=115200)
