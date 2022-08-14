import subprocess
import sys


def run_shell_command(command: str, cwd: str = None):
    p = subprocess.run(
        command.split(" "),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )
    assert p.returncode == 0, (
        f"command '{command}' failed with exit code "
        + f"{p.returncode}: stderr = '{p.stderr}'"
    )
    return p


def run():
    print(
        "Please DO NOT use a virtual environment for PYRA! Use the"
        + " system interpreter available via the command 'python'.\n\n"
        + f"Currently using the interpreter '{sys.executable}'"
    )

    if not input(
        f"\nOpen a new shell, run 'which python'. Is the system-"
        + "interpreter the same as the current interpreter? (Y/n) "
    ).startswith("Y"):
        print("aborting")
        return

    python_version = sys.version.split(" ")[0]
    assert python_version.startswith(
        "3.10."
    ), f"Please use Python 3.10.x (currently at {python_version})"

    # now we can assume that the system interpreter is used
    # and has a Python version 3.10.x

    try:
        run_shell_command("which poetry")
    except AssertionError as e:
        print(e)
        print(
            "Please make sure to have poetry installed. See "
            + "https://python-poetry.org/\naborting"
        )

    # now, all required system software can be assumed to be present
