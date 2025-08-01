from enum import Enum, auto


class Board(Enum):
    PICO2 = auto()
    PICO2_W = auto()


def from_name(name: str) -> Board:
    match name:
        case 'pico2':
            result = Board.PICO2
        case 'pico2-w':
            result = Board.PICO2_W
        case _:
            raise NotImplementedError

    return result
