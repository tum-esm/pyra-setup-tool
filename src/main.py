import os
import sys
from .routines.fetch_release_tags import fetch_release_tags
from .utils.get_documents_dir import get_documents_dir
from .utils.printing_utils import print_line, pretty_print
from .utils.run_shell_command import run_shell_command


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
            run_shell_command("poetry --version")
            pretty_print(f"Found poetry!", color="green")
        except AssertionError as e:
            pretty_print(
                "Please make sure to have poetry installed. See "
                + "https://python-poetry.org/",
                color="red",
            )
            raise e

        try:
            run_shell_command("tar --version")
            pretty_print(f"Found tar!", color="green")
        except AssertionError as e:
            pretty_print(
                "Please make sure to have tar installed. ",
                color="red",
            )
            raise e

        try:
            run_shell_command("gh --version")
            pretty_print(f"Found github cli!", color="green")
        except AssertionError as e:
            pretty_print(
                "Please make sure to have the github cli installed. "
                + "See https://github.com/cli/cli#installation",
                color="red",
            )
            raise e

        # now we can assume that all required system software is present
        print_line()

        documents_directory = get_documents_dir()
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
