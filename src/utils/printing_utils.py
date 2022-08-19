import os


def pretty_print(text: str, color: str | None = None, end: str = "\n"):
    color_sequences = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m"}
    if color is not None:
        assert color in color_sequences.keys(), f"Unknown color '{color}'"
        text = f"{color_sequences[color]}{text}\033[00m"
    print(text, end=end)


def print_line():
    print("-" * os.get_terminal_size().columns)
