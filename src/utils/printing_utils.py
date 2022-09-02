import os
from typing import Literal, Optional
from colorama import Fore, Style


def pretty_print(
    text: str,
    color: Optional[Literal["red", "green", "yellow"]] = None,
    end: str = "\n",
) -> None:
    color_sequences = {"red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW}
    if color is not None:
        text = color_sequences[color] + text + Style.RESET_ALL
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
