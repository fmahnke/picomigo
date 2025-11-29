from typing import Any, override

class Frame:
    length: int
    type: str
    message: str

    def __init__(self, length: int, type: str, message: str) -> None:
        pass

    @override
    def __str__(self) -> str:
        ...


def decode_message(payload: Any) -> Frame | None:
    ...
