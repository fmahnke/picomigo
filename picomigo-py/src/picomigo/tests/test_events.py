import unittest
from io import StringIO

from pico.modules.events import signal

_output = StringIO()

__all__ = ['TestEvents']


class TestEvents(unittest.TestCase):
    def test_connect(self):
        test_signal = signal('test_connect')

        _ = test_signal.connect(each)
        _ = test_signal.connect(round_two, sender=2)

        self.assertEqual(len(test_signal.receivers), 2)

    @unittest.expectedFailure
    def test_disconnect(self):
        test_signal = signal('test_disconnect')

        _ = test_signal.connect(each)
        _ = test_signal.connect(round_two, sender=2)

        _ = test_signal.disconnect(each)
        _ = test_signal.disconnect(round_two, sender=2)

        self.assertEqual(len(test_signal.receivers), 0)

    def test_send(self):
        started = signal('test_send')

        _ = started.connect(each)
        _ = started.connect(round_two, sender=2)

        self.assertEqual(len(started.receivers), 2)

        for round in range(1, 4):
            _ = started.send(round)

        _ = started.disconnect(each)
        _ = started.disconnect(round_two, sender=2)

        self.assertEqual(
            _output.getvalue(),
            '''Round 1
Round 2
This is round two.
Round 3
'''
        )


def each(round: int):
    print(f"Round {round}", file=_output)


def round_two(_: int):
    print("This is round two.", file=_output)


if __name__ == '__main__':
    _ = unittest.main()
