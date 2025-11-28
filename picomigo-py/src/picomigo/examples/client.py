"""
Host client using pyserial to talk to a Pico 2 running the example server.

Run on Linux host:
    uv run python src/picomigo/examples/client.py --port /dev/ttyACM0

Protocol: LEN|TYPE|PAYLOAD\\n (binary safe, line delimited).
Sends an initial `ping`, then a user message, and prints all frames received.
"""

import argparse
import threading
import time

import serial


def build_frame(frame_type: str, payload: bytes) -> bytes:
    header = f'{len(payload)}|{frame_type}|'.encode()

    frame = header + payload + b'\n'

    return frame


def reader_loop(port: serial.Serial, stop_flag: threading.Event) -> None:
    buffer: bytes = b''

    while not stop_flag.is_set():
        data = port.read(port.in_waiting or 1)

        if not data:
            continue

        buffer += data

        while True:
            newline_index = buffer.find(b'\n')

            if newline_index == -1:
                break

            line = buffer[:newline_index]

            buffer = buffer[newline_index + 1:]

            print(f'rx: {line.decode()}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Talk to a Pico server over USB CDC.'
    )

    parser.add_argument(
        '--port',
        default='/dev/ttyACM0',
        help='serial device path (e.g. /dev/ttyACM0)'
    )

    parser.add_argument(
        '--message',
        default='hello from host',
        help='payload to send after ping'
    )

    parser.add_argument(
        '--timeout',
        type=float,
        default=2.0,
        help='seconds to wait for responses before closing'
    )

    return parser.parse_args()


def run_client(port_name: str, message: str, timeout: float) -> None:
    with serial.Serial(port_name, baudrate=115200, timeout=0.1) as port:
        stop_flag = threading.Event()

        thread = threading.Thread(
            target=reader_loop, args=(port, stop_flag), daemon=True
        )

        thread.start()

        _ = port.write(build_frame('ping', b''))

        time.sleep(0.1)

        _ = port.write(build_frame('msg', message.encode()))

        time.sleep(timeout)

        stop_flag.set()

        thread.join()


def main() -> None:
    args = parse_args()

    run_client(args.port, args.message, args.timeout)


if __name__ == '__main__':
    main()
