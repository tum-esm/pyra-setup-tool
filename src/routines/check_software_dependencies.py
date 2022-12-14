import sys
from typing import Optional
from src.utils import shell_utils, printing_utils


def check_python_version() -> None:
    python_version = sys.version.split(" ")[0]
    assert python_version.startswith(
        "3.10."
    ), f"Please use Python 3.10.x (currently at {python_version})"

    printing_utils.pretty_print(f"Python version {python_version} is supported", color="green")


def check_command_availability(command: str, name: Optional[str] = None) -> None:
    pretty_command_name = command if name is None else name
    try:
        shell_utils.run_shell_command(f"{command} --version")
        printing_utils.pretty_print(f"Found {pretty_command_name}!", color="green")
    except AssertionError as e:
        printing_utils.pretty_print(
            f"Please make sure to have {pretty_command_name} installed.",
            color="red",
        )
        raise e


def check_setup_tool_version() -> None:
    pull_stdout = shell_utils.run_shell_command("git pull")
    if pull_stdout == "Already up to date.":
        printing_utils.pretty_print("Setup tool is up to date.", color="green")
    else:
        printing_utils.pretty_print("Updated the setup tool.")
        printing_utils.pretty_print(
            f"Please run the setup tool again!",
            color="yellow",
        )
        sys.exit()
