import time

import serial


def build_frame(frame_type: str, payload: bytes) -> bytes:
    header = f'{len(payload)}|{frame_type}|'.encode()

    frame = header + payload + b'\n'

    return frame


def main() -> None:
    with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.1) as port:
        while True:
            _ = port.write(build_frame('ping', b''))

            data = port.read(port.in_waiting or 1)

            if len(data) == 0:
                print('waiting...')

                time.sleep(1.0)

                continue

            output = data.decode('utf-8')

            print(output)

            time.sleep(1.0)


main()
