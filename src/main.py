import os
import subprocess
import sys


def pprint(text: str, color: str | None = None, end: str = "\n"):
    color_sequences = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m"}
    if color is not None:
        assert color in color_sequences.keys(), f"Unknown color '{color}'"
        text = f"{color_sequences[color]}{text}\033[00m"
    print(text, end=end)


def print_line():
    print("-" * os.get_terminal_size().columns)


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
        pprint("Welcome to the pyra-setup-tool! Instruction formatting: ")
        pprint("  * checkpoints are green ", color="green")
        pprint("  * todos are yellow ", color="yellow")
        pprint("  * errors are red ", color="red")
        pprint("  * information is uncolored ")
        print_line()

        pprint(
            "Please DO NOT use a virtual environment for PYRA! Use the"
            + " system interpreter available via the command 'python'. "
            + f"Currently using the interpreter '{sys.executable}'"
        )
        pprint(
            f"Run 'which python' in another shell. Are system-"
            + "interpreter and the current one identical? (Y/n) ",
            color="yellow",
            end="",
        )
        if not input().startswith("Y"):
            pprint("Aborting", color="red")
            return

        python_version = sys.version.split(" ")[0]
        assert python_version.startswith(
            "3.10."
        ), f"Please use Python 3.10.x (currently at {python_version})"

        # now we can assume that the used interpreter is correct
        pprint(f"Python version {python_version} is supported", color="green")

        try:
            run_shell_command("which poetry")
        except AssertionError as e:
            pprint(
                "Please make sure to have poetry installed. See "
                + "https://python-poetry.org/",
                color="red",
            )
            raise e

        # now we can assume that all required system software is present
        pprint(f"Found poetry!", color="green")
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
        pprint("Exception occured!", color="red")
        raise e
