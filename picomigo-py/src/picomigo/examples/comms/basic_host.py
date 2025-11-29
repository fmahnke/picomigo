import sys
import time

import msgpack
import serial
from mktech.log import log

from picomigo.pico.comms.message import Frame, decode_message


class BasicHost:
    _type: str

    def __init__(self) -> None:
        self._type = 'msgpack'
        self._streaming: bool = True

    def run(self):
        with serial.Serial('/dev/ttyACM0', baudrate=115200,
                           timeout=0.1) as port:
            buffer: bytes = b''

            if self._streaming:
                # message_accum = b''

                unpacker = msgpack.Unpacker(
                    port, max_buffer_size=128, object_hook=decode_message
                )

                while True:
                    message = None

                    log.debug(f'waiting: {port.in_waiting}')

                    # if port.in_waiting == 0:
                    #     data = port.read(1)

                    #     assert len(data) == 0

                    if port.in_waiting == 0:
                        _ = port.write(self._build_frame(b'hello'))
                    else:

                        try:
                            message = next(unpacker)

                            assert isinstance(message, Frame)
                            # message = msgpack.unpack(port, max_buffer_size=128)

                            # message_accum += message
                        except ValueError as e:
                            log.error(f'error: {e}')

                        log.info(f'message: {message}')
                        # log.info(
                        #     f'message_a ({len(message_accum)}): {message_accum}'
                        # )

                    time.sleep(0.5)
            else:
                count = 0

                count_max = 1

                while count < count_max:
                    log.debug('read')

                    data = port.read(port.in_waiting or 1)

                    log.debug(f'process data: {data}')

                    if data:
                        buffer += data

                        message: str | None = None

                        try:
                            message = msgpack.unpackb(buffer)
                        except msgpack.exceptions.ExtraData:
                            message = 'error: extra data'

                            buffer = b''

                        if message:
                            print(f'rx: {message}')

                    time.sleep(1)

                count_max += 1

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
