import sys
from src import utils


def check_python_version() -> None:
    """Checks if the Python version is 3.10.x."""

    python_version = sys.version.split(" ")[0]
    assert python_version.startswith("3.10."), (
        f"Please use Python 3.10.x (currently at {python_version})"
    )

    utils.pretty_print(f"Python version {python_version} is supported", color="green")


def check_command_availability(command: str) -> None:
    """Checks if a command is available on the system."""
    try:
        utils.run_shell_command(f"{command} --version")
        utils.pretty_print(f"Found {command}!", color="green")
    except AssertionError as e:
        utils.pretty_print(
            f"Please make sure to have {command} installed.",
            color="red",
        )
        raise e


def check_setup_tool_version() -> None:
    """Performs a `git pull` inside the setup tool directory to
    check if the setup tool is up to date.

    If it is not up to date, it will print a message and exit
    because the user needs to run the setup tool again in order
    to run the setup tool using the newest code."""

    pull_stdout = utils.run_shell_command("git pull")
    if pull_stdout == "Already up to date.":
        utils.pretty_print("Setup tool is up to date.", color="green")
    else:
        utils.pretty_print("Updated the setup tool.")
        utils.pretty_print(
            f"Please run the setup tool again!",
            color="yellow",
        )
        sys.exit()
