from os.path import isfile

from mktech.error import Err, Error, Ok, Result
from mktech.log import log

from .board import Board
from .config import BuildConfig
from .runner import picotool


def execute(target: str, board: Board,
            build_config: BuildConfig) -> Result[None, Error]:
    match target:
        case 'micropython' | 'upython':
            top_build_path = f'{build_config.micropython_source_dir}/ports/rp2/build'  # noqa: E501

            match board:
                case Board.PICO2:
                    board_path = 'RPI_PICO2'
                case Board.PICO2_W:
                    board_path = 'RPI_PICO2_W'

            target_path = f'{top_build_path}-{board_path}/firmware.uf2'
        case _:
            # Try target as a path on the filesystem

            if isfile(target):
                target_path = target
            else:
                return Err(Error(f'target file not found: {target}'))

    log.info(f'load {target_path}')

    match picotool.load(f'-f {target_path}'):
        case Err(e):
            return Err(e)
        case Ok(_):
            pass

    return picotool.reboot()
