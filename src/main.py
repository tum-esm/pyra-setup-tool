import sys

try:
    import colorama
except ImportError:
    print('Please run "pip install colorama" first')
    sys.exit()

colorama.init()

from src.utils import directory_utils, printing_utils
from src import commands, tasks


def run() -> None:
    try:
        printing_utils.print_line()
        printing_utils.pretty_print("Welcome to the pyra-setup-tool! Instruction formatting: ")
        printing_utils.pretty_print("  * checkpoints = green ", color="green")
        printing_utils.pretty_print("  * expecting user input = yellow ", color="yellow")
        printing_utils.print_line()

        # The following check is necessary because I did not manage to de-
        # activate the current venv from within a subprocess/system call/etc.
        printing_utils.pretty_print(
            "Please DO NOT use a virtual environment for PYRA! Use the"
            + " system interpreter available via the command 'python'. "
            + f"Currently using the interpreter '{sys.executable}'"
        )
        if not printing_utils.pretty_input(
            f"Run 'which python' in another shell. Are system-"
            + "interpreter and the current one identical?",
            ["Y", "n"],
        ).startswith("Y"):
            printing_utils.pretty_print("Aborting", color="red")
            return

        tasks.check_software_dependencies.check_python_version()
        tasks.check_software_dependencies.check_command_availability("poetry")
        tasks.check_software_dependencies.check_command_availability("tar")
        tasks.check_software_dependencies.check_command_availability("git")
        tasks.check_software_dependencies.check_command_availability("gh", name="github cli")
        tasks.check_software_dependencies.check_setup_tool_version()

        pyra_directory = directory_utils.initialize_pyra_directories()
        printing_utils.pretty_print(
            f'Successfully initialized local environment inside "{pyra_directory}"',
            color="green",
        )

        # Now we can assume that the required system state is present
        # (software dependencies and code/ui directories)

        # Infinite loop (waiting for new command -> execute command -> ...)
        while True:
            printing_utils.print_line()
            command = printing_utils.pretty_input(
                "Enter a command",
                ["help", "status", "install", "rollback", "remove", "exit"],
            )

            if command == "help":
                print("status: check the installation status")
                print("    * list locally install versions")
                print("    * list available release version")
                print("    * show, if pyra-cli command is installed in environment path")
                print("    * show which pyra version the cli-command currently uses")
                print("install: install a new version from GitHub")
                print("    * choose an available release version")
                print("    * download code from github")
                print("    * install dependencies")
                print("    * download UI and run windows installer")
                print("    * set the pyra-cli to point to the new version")
                print("    * test if pyra-cli command is installed in environment path")
                print("    * add desktop-shortcut to code directory")
                print("    * migrate config from an older version")
                print("rollback: (use an old local version again)")
                print("    * run the installer for an already existing UI version")
                print("    * set the pyra-cli to point to the new version")
                print("    * test if pyra-cli command is installed in environment path")
                print("    * add desktop-shortcut to code directory")
                print("remove: remove a locally installed version")

            if command == "status":
                commands.status.run()

            elif command == "install":
                commands.install.run()

            elif command == "rollback":
                commands.rollback.run()

            elif command == "remove":
                commands.remove.run()

            elif command == "exit":
                print("Exiting program")
                return

            else:
                printing_utils.pretty_print(f'Unknown command "{command}"', color="red")

    except KeyboardInterrupt:
        printing_utils.pretty_print("Exiting program")
    except Exception as e:
        printing_utils.pretty_print("Exception occured!", color="red")
        raise e
