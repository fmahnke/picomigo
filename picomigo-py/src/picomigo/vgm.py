from io import StringIO

from mktech.error import Err, Error, Ok, Result
from mktech.path import Path

from .audio.vgm import VgmOutputFormat, VgmParser


def main(path: Path, format: str | None) -> Result[None, Error]:
    match format:
        case 'c':
            format_ = VgmOutputFormat.C_ARRAY
        case None:
            format_ = VgmOutputFormat.STRING
        case _:
            return Err(Error(f'unsupported format: {format}'))

    parser = VgmParser.create(path)

    output = StringIO()

    parser.format_command_list(output, format_)

    print(output.getvalue())

    print(parser.metadata)

    return Ok(None)
