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
import umsgpack
import uselect

from .message import Frame, decode_message

FrameHandler = Callable[[str, bytes], None]


class InvalidMessageError(Exception):
    pass


class Comms:
    _buffer: bytes

    def __init__(self) -> None:
        self._streaming: bool = True
        self._sending: bool = False

        self._buffer = b''

        self._poller: uselect.poll = uselect.poll()

        self._poller.register(sys.stdin.buffer, uselect.POLLIN)

    async def read_frames(self) -> None:
        if self._streaming:
            while True:
                frame = self._receive()

                if frame is None:
                    # self._send_log('incomplete frame')

                    continue

                self._send_log(f'frame data: {frame}')

                self._buffer = b''

                self._handle_frame(frame)

                await asyncio.sleep_ms(1000)
        else:
            if self._sending:
                count = 0

                count_max = 10

                while count < count_max:
                    self._send_log(f'count: {count}')

                    count += 1

                    await asyncio.sleep_ms(1000)
            else:
                while True:
                    events = self._poller.poll(0)

                    if events:
                        # self._send_log('got event')

                        chunk = sys.stdin.buffer.read(1)

                        if not chunk:
                            # self._send_log('waiting...')

                            await asyncio.sleep_ms(1000)

                            continue

                        # self._send_log(f'got chunk: {chunk}')

                        self._buffer += chunk

                        # self._send_log(
                        #     f'read frame from buffer: {self._buffer}'
                        # )

                        frame = self._receive()

                        if frame is None:
                            # self._send_log('incomplete frame')

                            continue

                        # self._send_log(f'frame data: {frame}')

                        self._buffer = b''

                        self._handle_frame(frame)

                    await asyncio.sleep_ms(1000)

    def _send(self, payload: bytes) -> None:
        _ = sys.stdout.buffer.write(payload)

    # def _read_frame(self, type: str = 'msg') -> Frame | None:
    #     self._send_log(f'read frame from buffer: {self._buffer}')

    #     result = umsgpack.loads(self._buffer)

    #     self._send_log(f'frame data: {result}')

    #     return None, 'msg', result

    def _receive(self) -> Frame | None:
        if self._streaming:
            payload = umsgpack.load(sys.stdin.buffer)

            if payload is None:
                result = None
            else:
                if not (isinstance(payload, dict) and 'length' in payload
                        and 'type' in payload and 'message' in payload):
                    result = None
                else:
                    result = Frame(
                        length=payload['length'],
                        type=payload['type'],
                        message=payload['message']
                    )
        else:
            try:
                payload = umsgpack.loads(self._buffer)
            except umsgpack.InsufficientDataException:
                payload = None

            if payload is None:
                result = None
            else:
                if not (isinstance(payload, dict) and 'length' in payload
                        and 'type' in payload and 'message' in payload):
                    result = None
                else:
                    result = Frame(
                        length=payload['length'],
                        type=payload['type'],
                        message=payload['message']
                    )

        return result

    def _build_frame(self, frame_type: str, payload: bytes) -> bytes:
        frame_ = Frame(len(payload), frame_type, payload.decode('utf-8'))

        frame = umsgpack.dumps(
            {
                'length': frame_.length,
                'type': frame_.type,
                'message': frame_.message
            }
        )

        return frame

    def _send_frame(self, frame_type: str, payload: bytes) -> None:
        frame = self._build_frame(frame_type, payload)

        _ = sys.stdout.buffer.write(frame)

    def _send_log(self, message: str) -> None:
        if not message.endswith('\n'):
            message += '\n'

        self._send_frame('log', message.encode('utf-8'))

    def _handle_frame(self, frame: Frame) -> None:
        # self._send_log(f'got frame type: {frame.type}')

        if frame.type == 'ping':
            self._send_frame('pong', b'')
        elif frame.type == 'msg':
            self._send_frame('ok', frame.message.encode())
        else:
            self._send_frame('err', b'unknown type')


async def main() -> None:
    server = Comms()

    await server.read_frames()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
