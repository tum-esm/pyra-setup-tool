import os
import subprocess
import sys
from .utils.fetch_release_tags import fetch_release_tags
from .utils.printing_utils import print_line, pretty_print
from .utils import types


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
    try:
        print_line()
        pretty_print("Welcome to the pyra-setup-tool! Instruction formatting: ")
        pretty_print("  * checkpoints are green ", color="green")
        pretty_print("  * todos are yellow ", color="yellow")
        pretty_print("  * errors are red ", color="red")
        pretty_print("  * information is uncolored ")
        print_line()

        pretty_print(
            "Please DO NOT use a virtual environment for PYRA! Use the"
            + " system interpreter available via the command 'python'. "
            + f"Currently using the interpreter '{sys.executable}'"
        )
        pretty_print(
            f"Run 'which python' in another shell. Are system-"
            + "interpreter and the current one identical? (Y/n) ",
            color="yellow",
            end="",
        )
        if not input().startswith("Y"):
            pretty_print("Aborting", color="red")
            return

        python_version = sys.version.split(" ")[0]
        assert python_version.startswith(
            "3.10."
        ), f"Please use Python 3.10.x (currently at {python_version})"

        # now we can assume that the used interpreter is correct
        pretty_print(f"Python version {python_version} is supported", color="green")

        try:
            run_shell_command("which poetry")
        except AssertionError as e:
            pretty_print(
                "Please make sure to have poetry installed. See "
                + "https://python-poetry.org/",
                color="red",
            )
            raise e

        # now we can assume that all required system software is present
        pretty_print(f"Found poetry!", color="green")
        print_line()

        documents_directory = get_documents_directory()
        assert os.path.isdir(
            documents_directory
        ), f"Documents directory does not exist. ({documents_directory})"

        pyra_directory = os.path.join(documents_directory, "pyra")
        if not os.path.isdir(pyra_directory):
            os.mkdir(pyra_directory)
            print(f"Created directory '{pyra_directory}'")

        local_pyra_versions = get_local_pyra_versions(pyra_directory)
        if len(local_pyra_versions) == 0:
            print("Did not find any local pyra versions.")
        else:
            print(f"local pyra versions: {', '.join(local_pyra_versions)}")

        # TODO: infinite loop (select from install|uninstall|abort)

    except Exception as e:
        pretty_print("Exception occured!", color="red")
        raise e


if __name__ == "__main__":
    print(fetch_release_tags())
