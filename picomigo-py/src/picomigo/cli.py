import sys

import click
from mktech.log import log
from mktech.path import Path

from . import build, native_check, run, serial

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
def cli() -> None:
    log.remove()
    _ = log.add(sys.stderr, level='INFO')


@cli.command()
def build_command() -> None:
    build.build()


@cli.command()
@click.argument('path', required=False, type=click.Path(path_type=Path))
@click.option('--verbose', '-v', count=True)
def native_check_command(path: Path | None, verbose: int) -> None:
    native_check.main(path, verbose)


@cli.command()
def run_command() -> None:
    run.run()


@cli.command()
def serial_command() -> None:
    serial.main()


def main() -> None:
    cli()
