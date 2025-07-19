import pytest

from pico_dev import cli


def test_main() -> None:
    """Basic CLI test."""

    with pytest.raises(SystemExit):
        cli.main()
