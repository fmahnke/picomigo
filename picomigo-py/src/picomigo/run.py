import sys
import time

# from mktech.serial_port import Serial


def run() -> None:
    print('ok')

    while True:
        data = sys.stdin.read()

        print(f'data={data}')

        time.sleep(1)
    '''
    with Serial('/dev/ttyACM0', baudrate=115200, timeout=1) as serial:
        while True:
            if serial.in_waiting != 0:
                data = serial.readlines()

                print(data)
    '''  # pyright: ignore[reportUnreachable]
