from io import StringIO

import pytest
from mktech import resources
from mktech.log import log
from picomigo.audio import vgm

p = resources.resource_path(
    'tests.audio.resources.game_gear', 'battletoads - surf city.vgm'
).unwrap()


@pytest.fixture
def parser():
    data = p.read_bytes()

    parser = vgm.Parser(data)

    return parser


class TestParser:
    def test_parser(self, parser) -> None:
        log.debug(parser)

        parser.parse_metadata()

        log.debug(parser.metadata)

        parser.parse_gd3()

        log.debug(parser.gd3_data)

        parser.parse_commands()

        log.debug(parser.command_list)

    def test_format_command_list(self, parser) -> None:
        parser.parse_commands()

        output = StringIO()

        parser.format_command_list(output)

        log.debug(output.getvalue())

    def test_format_command_list_c_array(self, parser) -> None:
        parser.parse_commands()

        output = StringIO()

        parser.format_command_list(output, vgm.CommandFormat.C_ARRAY)

        log.debug(output.getvalue())
