import os
from typing import Literal, Optional


def pretty_print(
    text: str,
    color: Optional[Literal["red", "green", "yellow"]] = None,
    end: str = "\n",
) -> None:
    color_sequences = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m"}
    if color is not None:
        text = f"{color_sequences[color]}{text}\033[00m"
    print(text, end=end)


def print_line() -> None:
    print("-" * os.get_terminal_size().columns)


def pretty_input(message: str, options: list[str]) -> str:
    pretty_print(
        f"{message} ({' | '.join(options)}) ",
        color="yellow",
        end="",
    )
    return input().strip()
