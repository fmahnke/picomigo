from mktech import resources
from mktech.log import log
from picomigo.audio import vgm

p = resources.resource_path(
    'tests.audio.resources.game_gear', 'battletoads - surf city.vgm'
).unwrap()


class TestParser:
    def test_parser(self) -> None:
        data = p.read_bytes()

        parser = vgm.Parser(data)

        log.debug(parser)

        parser.parse_metadata()

        log.debug(parser.metadata)

        parser.parse_gd3()

        log.debug(parser.gd3_data)

        parser.parse_commands()

        log.debug(parser.command_list)
