import os
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


def get_documents_directory():
    if sys.platform in ["darwin", "linux"]:
        return os.environ["HOME"] + "/Documents"
    elif sys.platform in ["win32", "cygwin"]:
        return os.environ["USERPROFILE"] + "\\Documents"
    else:
        raise Exception(f"Unknown platform '{sys.platform}'")


def get_local_pyra_versions(pyra_directory: str):
    return [
        d
        for d in os.listdir(pyra_directory)
        if (d.startswith("pyra-") and os.path.isdir(os.path.join(pyra_directory, d)))
    ]


def run():
    print(
        "Please DO NOT use a virtual environment for PYRA! Use the"
        + " system interpreter available via the command 'python'. "
        + f"Currently using the interpreter '{sys.executable}'"
    )
    if not input(
        f"TODO: Run 'which python' in another shell. Do system-"
        + "interpreter and the current one match? (Y/n) "
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
        print(
            "Please make sure to have poetry installed. See "
            + "https://python-poetry.org/\naborting"
        )
        raise e

    # now, all required system software can be assumed to be present

    documents_directory = get_documents_directory()
    assert os.path.isdir(
        documents_directory
    ), f"Documents directory does not exist. ({documents_directory})"

    pyra_directory = os.path.join(documents_directory, "pyra")
    if not os.path.isdir(pyra_directory):
        os.mkdir(pyra_directory)
        print(f"Created directory '{pyra_directory}'")

    local_pyra_versions = get_local_pyra_versions(pyra_directory)
    print(
        f"Local PYRA versions: {', '.join(local_pyra_versions)}"
        + f"{'none' if len(local_pyra_versions) == 0 else ''}"
    )
