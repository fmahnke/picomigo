from typing import Any


class Frame:
    length: int
    type: str
    message: str

    def __init__(self, length: int, type: str, message: str) -> None:
        self.length = length
        self.type = type
        self.message = message

    def __str__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        return (
            f'<Frame length={self.length}, type={self.type}'
            + f', message="{self.message}">'
        )


def decode_message(payload: Any) -> Frame | None:
    return Frame(**payload)


# def decode_message(payload: Any) -> Frame | None:
#     length = payload[0]

#     message = payload[1]

#     if len(message) != length:
#         result = None
#     else:
#         result = Frame(length, 'msg', message)

#     return result
