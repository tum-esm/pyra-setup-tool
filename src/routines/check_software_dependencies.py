import sys
from src.utils import shell_utils, printing_utils


def check_python_version() -> None:
    python_version = sys.version.split(" ")[0]
    assert python_version.startswith(
        "3.10."
    ), f"Please use Python 3.10.x (currently at {python_version})"

    printing_utils.pretty_print(
        f"Python version {python_version} is supported", color="green"
    )


def check_poetry_availability() -> None:
    try:
        shell_utils.run_shell_command("poetry --version")
        printing_utils.pretty_print(f"Found poetry!", color="green")
    except AssertionError as e:
        printing_utils.pretty_print(
            "Please make sure to have poetry installed. See "
            + "https://python-poetry.org/",
            color="red",
        )
        raise e


def check_tar_availability() -> None:
    try:
        shell_utils.run_shell_command("tar --version")
        printing_utils.pretty_print(f"Found tar!", color="green")
    except AssertionError as e:
        printing_utils.pretty_print(
            "Please make sure to have tar installed. ",
            color="red",
        )
        raise e


def check_github_cli_availability() -> None:
    try:
        shell_utils.run_shell_command("gh --version")
        printing_utils.pretty_print(f"Found github cli!", color="green")
    except AssertionError as e:
        printing_utils.pretty_print(
            "Please make sure to have the github cli installed. "
            + "See https://github.com/cli/cli#installation",
            color="red",
        )
        raise e
