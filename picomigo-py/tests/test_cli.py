import pytest

from picomigo import cli


def test_main() -> None:
    """Basic CLI test."""

    with pytest.raises(SystemExit):
        cli.main()
