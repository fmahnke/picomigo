import click

from . import build, run, serial

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
def cli() -> None:
    pass


@cli.command()
def build_command() -> None:
    build.build()


@cli.command()
def run_command() -> None:
    run.run()


@cli.command()
def serial_command() -> None:
    serial.main()


def main() -> None:
    cli()
