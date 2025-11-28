"""
Minimal MicroPython server for Pico 2 using USB CDC stdin/stdout.

Run on the board:
    mpremote run src/picomigo/examples/server.py

Protocol: LEN|TYPE|PAYLOAD\\n (binary safe, line delimited).
Handles `ping` (responds `pong`), `msg` (echoes with `ok`), otherwise `err`.
"""

try:
    from typing import Callable, Tuple
except ImportError:

    class _Subscriptable:
        def __getitem__(self, item):
            return object

    Callable = _Subscriptable()  # type: ignore
    Tuple = _Subscriptable()  # type: ignore

import sys

import uasyncio as asyncio
import uselect

FrameHandler = Callable[[str, bytes], None]
Frame = Tuple[int, str, bytes]


def build_frame(frame_type: str, payload: bytes) -> bytes:
    header = f'{len(payload)}|{frame_type}|'.encode()

    frame = header + payload + b'\n'

    return frame


def send_frame(frame_type: str, payload: bytes) -> None:
    frame = build_frame(frame_type, payload)

    _ = sys.stdout.buffer.write(frame + b'\n')

    try:
        sys.stdout.buffer.flush()
    except AttributeError:
        pass

    try:
        sys.stdout.flush()
    except AttributeError:
        pass


def parse_frame(line: bytes) -> Frame | None:
    try:
        length_text, frame_type, payload_text = line.decode().split('|', 2)
    except ValueError:
        return None

    try:
        length = int(length_text)
    except ValueError:
        return None

    payload = payload_text.encode()

    if len(payload) != length:
        return None

    return length, frame_type, payload


async def read_frames(handler: FrameHandler) -> None:
    poller = uselect.poll()

    poller.register(sys.stdin.buffer, uselect.POLLIN)

    buffer: bytes = b''

    while True:
        events = poller.poll(0)

        if events:
            # print('got event')

            chunk = sys.stdin.buffer.read(1)

            if not chunk:
                # print('waiting...')

                await asyncio.sleep_ms(1000)

                continue

            # print(f'got chunk: {chunk}')

            buffer += chunk

            while True:
                # print('parse frame')

                newline_index = buffer.find(b'\n')

                if newline_index == -1:
                    break

                line = buffer[:newline_index]

                buffer = buffer[newline_index + 1:]

                print(f'parsing frame line: "{line}"')

                frame = parse_frame(line)

                if frame is None:
                    send_frame('err', b'bad frame')

                    continue

                _, frame_type, payload = frame

                handler(frame_type, payload)

        await asyncio.sleep_ms(5)


def handle_frame(frame_type: str, payload: bytes) -> None:
    print(f'got frame type: {frame_type}')

    if frame_type == 'ping':
        send_frame('pong', b'')
    elif frame_type == 'msg':
        send_frame('ok', payload)
    else:
        send_frame('err', b'unknown type')


async def main() -> None:
    print('pico server ready')

    await read_frames(handle_frame)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
