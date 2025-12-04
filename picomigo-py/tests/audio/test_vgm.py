from io import StringIO

import pytest
from mktech import resources
from mktech.log import log
from picomigo.audio.vgm import VgmOutputFormat, VgmParser

p = resources.resource_path(
    'tests.audio.resources.game_gear', 'battletoads - surf city.vgm'
).unwrap()


@pytest.fixture
def parser():
    parser = VgmParser.create(p)

    return parser


class TestParser:
    def test_parser(self, parser: VgmParser) -> None:
        log.debug(parser)

        log.debug(parser.metadata)

        log.debug(parser.gd3_data)

        log.debug(parser.command_list)

    def test_format_command_list(self, parser: VgmParser) -> None:
        output = StringIO()

        parser.format_command_list(output)

        log.debug(output.getvalue())

    def test_format_command_list_c_array(self, parser: VgmParser) -> None:
        output = StringIO()

        parser.format_command_list(output, VgmOutputFormat.C_ARRAY)

        log.debug(output.getvalue())
