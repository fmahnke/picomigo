from io import StringIO

from mktech.error import Err, Error, Ok, Result
from mktech.path import Path

from .audio.vgm import CommandFormat, Parser


def main(path: Path, format: str | None) -> Result[None, Error]:
    match format:
        case 'c':
            format_ = CommandFormat.C_ARRAY
        case None:
            format_ = CommandFormat.STRING
        case _:
            return Err(Error(f'unsupported format: {format}'))

    data = path.read_bytes()

    parser = Parser(data)

    output = StringIO()

    parser.format_command_list(output, format_)

    print(output.getvalue())

    print(parser.metadata)

    return Ok(None)
