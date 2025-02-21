import subprocess
import os
from os.path import dirname
from colorama import Fore, Style
from typing import Literal, Optional

PROJECT_DIR = dirname(dirname(dirname(os.path.abspath(__file__))))


def run_shell_command(
    command: str,
    cwd: str = PROJECT_DIR,
    silent: bool = True,
) -> str:
    """Runs a shell command and returns the stdout as a string.

    The command is silent by default, meaning that it does not
    print anything to the console."""

    print(f'Running command "{command}" in directory "{cwd}"')
    if silent:
        p = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
        )
        try:
            stdout = p.stdout.decode("utf-8", errors="replace")
            stderr = p.stderr.decode("utf-8", errors="replace")
        except Exception as e:
            print(f"Error when decoding p: {p}")
            raise e
    else:
        p = subprocess.run(command, shell=True, cwd=cwd)
        stdout = "null"
        stderr = "null"

    assert p.returncode == 0, (
        f"command '{command}' failed with exit code {p.returncode}: stderr = '{stderr}'"
    )
    return stdout.strip()


def pretty_print(
    text: str,
    color: Optional[Literal["red", "green", "yellow"]] = None,
    bold: bool = False,
    end: str = "\n",
) -> None:
    color_sequences = {"red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW}
    if color is not None:
        text = color_sequences[color] + text + Style.RESET_ALL
    if bold:
        text = Style.BRIGHT + text + Style.RESET_ALL
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
