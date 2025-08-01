from .board import Board


def board(board: Board) -> str:
    match board:
        case Board.PICO2:
            result = 'RPI_PICO2'
        case Board.PICO2_W:
            result = 'RPI_PICO2_W'

    return result
