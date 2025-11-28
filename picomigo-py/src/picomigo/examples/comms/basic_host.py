import time

import serial
from mktech.log import log


def build_frame(frame_type: str, payload: bytes) -> bytes:
    header = f'{len(payload)}|{frame_type}|'.encode()

    frame = header + payload + b'\n'

    return frame


def main():
    with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.1) as port:
        buffer: bytes = b''

        while True:
            log.info('read')

            data = port.read(port.in_waiting or 1)

            log.info(f'process data: {data}')

            if data:
                buffer += data

                while True:
                    newline_index = buffer.find(b'\n')

                    if newline_index == -1:
                        break

                    line = buffer[:newline_index]

                    buffer = buffer[newline_index + 1:]

                    print(f'rx: {line.decode()}')

            _ = port.write(build_frame('ping', b''))

            time.sleep(1)


if __name__ == '__main__':
    main()
