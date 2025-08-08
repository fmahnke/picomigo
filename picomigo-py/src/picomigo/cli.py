import sys
from dataclasses import dataclass

import click
from mktech.cli import from_config
from mktech.error import Err, Ok
from mktech.log import log
from mktech.path import Path

from . import board as board_module
from . import build, load, native_check, run, serial, vgm
from .config import BuildConfig


@dataclass
class CliContext():
    config: BuildConfig


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@from_config(BuildConfig, shorten={'log_level': '-l'})
@click.pass_context
def cli(ctx: click.Context, build_config: BuildConfig) -> None:
    _ = log.configure(
        **{
            'handlers':
                [{
                    'sink': sys.stderr,
                    'level': build_config.log_level,
                }, ],
            'activation': [
                ('sarge', False),
                ('sarge.parse', False),
            ]  # noqa: E122
        }  # pyright: ignore[reportArgumentType]
    )

    ctx.obj = CliContext(build_config)


@cli.command()
def build_command() -> None:
    build.build()


@cli.command()
@click.argument('path', required=False, type=click.Path(path_type=Path))
@click.option('--verbose', '-v', count=True)
def native_check_command(path: Path | None, verbose: int) -> None:
    native_check.main(path, verbose)


@cli.command()
@click.pass_context
@click.option('--board', '-b', required=True)
@click.argument('target')
def load_command(ctx: click.Context, target: str, board: str) -> None:
    board_ = board_module.from_name(board)

    match load.execute(target, board_, ctx.obj.config):
        case Err(e):
            print(e)
        case Ok(_):
            pass


@cli.command()
def run_command() -> None:
    run.run()


@cli.command()
def serial_command() -> None:
    serial.main()


@cli.command()
@click.argument('path', type=click.Path(path_type=Path))
@click.option('--format', '-f')
def vgm_command(path: Path, format: str | None) -> None:
    match vgm.main(path, format):
        case Err(e):
            print(e)
        case Ok(_):
            pass


def main() -> None:
    cli()
