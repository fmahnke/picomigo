import time

import msgpack
import serial
from mktech.log import log
from picomigo.pico.comms.message import Frame, decode_message


class RemotePeer:
    _connection: serial.Serial
    _unpacker: msgpack.Unpacker

    def __init__(self) -> None:
        self._connection = serial.Serial(
            '/dev/ttyACM0', baudrate=115200, timeout=0.1
        )

        self._unpacker = msgpack.Unpacker(
            self._connection,  # pyright: ignore[reportArgumentType]
            max_buffer_size=128,
            object_hook=decode_message,
        )

    def receive(self) -> list[Frame]:
        results: list[Frame] = []

        while True:
            message = None

            log.debug(f'waiting: {self._connection.in_waiting}')

            if self._connection.in_waiting == 0:
                break
            else:
                try:
                    message = next(self._unpacker)

                    log.debug(f'message={message}')

                except ValueError as e:
                    log.error(f'error: {e}')

                log.info(f'message: {message}')

                if not isinstance(message, Frame):
                    log.error(f'message type {type(message)} not expected')
                else:
                    results.append(message)

        return results

    def send(self, message: str) -> None:
        _ = self._connection.write(self._build_frame(message.encode()))

    def _build_frame(self, payload: bytes) -> bytes:
        length = len(payload)

        frame_ = Frame(length, 'msg', payload.decode('utf-8'))

        frame = msgpack.packb(frame_, default=encode_frame)

        return frame


def encode_frame(frame: Frame):
    return {
        'length': frame.length, 'type': frame.type, 'message': frame.message
    }
