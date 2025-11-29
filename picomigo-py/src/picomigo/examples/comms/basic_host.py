import sys
import time

from mktech.log import log

from picomigo.pico.comms.remote_peer import RemotePeer


class BasicHost:
    _client: RemotePeer

    def __init__(self) -> None:
        self._client = RemotePeer()

    def run(self):
        count = 0

        while True:
            messages = self._client.receive()

            if len(messages) == 0:
                self._client.send(f'count: {count}')
            else:
                for index, message in enumerate(messages):
                    print(f'{index}: {message}')

            count = 1

            time.sleep(0.5)


if __name__ == '__main__':
    log.remove()

    _ = log.add(sys.stderr, level='DEBUG')

    BasicHost().run()
