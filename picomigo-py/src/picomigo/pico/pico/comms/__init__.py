"""
Minimal MicroPython server for Pico 2 using USB CDC stdin/stdout.

Run on the board:
    mpremote run src/picomigo/examples/server.py

Protocol: LEN|TYPE|PAYLOAD\\n (binary safe, line delimited).
Handles `ping` (responds `pong`), `msg` (echoes with `ok`), otherwise `err`.
"""

import sys

import uasyncio as asyncio
import umsgpack

from .message import Frame


class InvalidMessageError(Exception):
    pass


class LocalPeer:
    def __init__(self) -> None:
        pass

    async def read_frames(self) -> None:
        while True:
            frame = self._receive()

            if frame is None:
                # self._send_log('incomplete frame')

                continue

            self._send_log(f'frame data: {frame}')

            self._handle_frame(frame)

            await asyncio.sleep_ms(1000)

    def _send(self, payload: bytes) -> None:
        _ = sys.stdout.buffer.write(payload)

    def _receive(self) -> Frame | None:
        payload = umsgpack.load(sys.stdin.buffer)

        if payload is None:
            result = None
        else:
            if not (isinstance(payload, dict) and 'length' in payload
                    and 'type' in payload and 'message' in payload):
                result = None
            else:
                result = Frame(
                    **payload  # pyright: ignore[reportUnknownArgumentType]
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
    server = LocalPeer()

    await server.read_frames()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
