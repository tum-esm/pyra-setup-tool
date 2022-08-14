import subprocess
import sys


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
