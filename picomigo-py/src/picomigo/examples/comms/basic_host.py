import sys
import time

import msgpack
import serial
from mktech.log import log

from picomigo.pico.comms.message import Frame, decode_message


class BasicHost:
    def __init__(self) -> None:
        pass

    def run(self):
        with serial.Serial('/dev/ttyACM0', baudrate=115200,
                           timeout=0.1) as port:
            unpacker = msgpack.Unpacker(
                port,  # pyright: ignore[reportArgumentType]
                max_buffer_size=128,
                object_hook=decode_message,
            )

            while True:
                message = None

                log.debug(f'waiting: {port.in_waiting}')

                if port.in_waiting == 0:
                    _ = port.write(self._build_frame(b'hello'))
                else:

                    try:
                        message = next(unpacker)

                        log.debug(f'message={message}')

                        assert isinstance(message, Frame)
                    except ValueError as e:
                        log.error(f'error: {e}')

                    log.info(f'message: {message}')

                time.sleep(0.5)

    def _build_frame(self, payload: bytes) -> bytes:
        length = len(payload)

        frame_ = Frame(length, 'msg', payload.decode('utf-8'))

        frame = msgpack.packb(frame_, default=encode_frame)

        return frame


def encode_frame(frame: Frame):
    return {
        'length': frame.length, 'type': frame.type, 'message': frame.message
    }


if __name__ == '__main__':
    log.remove()

    _ = log.add(sys.stderr, level='DEBUG')

    BasicHost().run()
