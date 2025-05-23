import sys

try:
    import colorama
except ImportError:
    print('Please run "pip install colorama" first')
    sys.exit()

colorama.init()

from src import utils, commands, tasks


def run() -> None:
    """The main entry point of the program.

    The program is structured as a loop that waits for user input and
    executes the corresponding command. The loop is terminated by the
    user entering the command "exit".

    Available commands: `help`, `status`, `install`, `rollback`,
    `remove`, `exit`"""

    try:
        utils.print_line()
        utils.pretty_print("Welcome to the pyra-setup-tool! Instruction formatting: ")
        utils.pretty_print("  * checkpoints = green ", color="green")
        utils.pretty_print("  * expecting user input = yellow ", color="yellow")
        utils.print_line()

        # The following check is necessary because I did not manage to de-
        # activate the current venv from within a subprocess/system call/etc.
        utils.pretty_print(
            "Please DO NOT use a virtual environment for PYRA! Use the"
            + " system interpreter available via the command 'python'. "
            + f"Currently using the interpreter '{sys.executable}'"
        )
        if not utils.pretty_input(
            f"Run 'which python' in another shell. Are system-"
            + "interpreter and the current one identical?",
            ["Y", "n"],
        ).startswith("Y"):
            utils.pretty_print("Aborting", color="red")
            return

        tasks.check_environment.check_python_version()
        tasks.check_environment.check_command_availability("curl")
        tasks.check_environment.check_command_availability("tar")
        tasks.check_environment.check_command_availability("git")
        tasks.check_environment.check_setup_tool_version()

        pyra_directory = utils.initialize_pyra_directories()
        utils.pretty_print(
            f'Successfully initialized local environment inside "{pyra_directory}"',
            color="green",
        )

        # Now we can assume that the required system state is present
        # (software dependencies and code/ui directories)

        # Infinite loop (waiting for new command -> execute command -> ...)
        while True:
            utils.print_line()
            command = utils.pretty_input(
                "Enter a command",
                ["help", "status", "install", "install-prerelease", "rollback", "remove", "exit"],
            )

            if command == "help":
                # fmt: off
                utils.pretty_print("status: check the installation status", bold=True)
                print("    * list locally install versions")
                print("    * list available release version")
                print("    * show, if pyra-cli command is installed in environment path")
                print("    * show which pyra version the cli-command currently uses")
                utils.pretty_print("install: install a new version from GitHub", bold=True)
                print("    * choose an available release version")
                print("    * download code from github")
                print("    * install dependencies")
                print("    * download UI and run windows installer")
                print("    * set the pyra-cli to point to the new version")
                print("    * test if pyra-cli command is installed in environment path")
                print("    * add desktop-shortcut to code directory")
                print("    * migrate config from an older version")
                utils.pretty_print("install-prerelease: same as install, but with prerelease versions", bold=True)
                utils.pretty_print("rollback: (use an old local version again)", bold=True)
                print("    * run the installer for an already existing UI version")
                print("    * set the pyra-cli to point to the new version")
                print("    * test if pyra-cli command is installed in environment path")
                print("    * add desktop-shortcut to code directory")
                utils.pretty_print("remove: remove a locally installed version", bold=True)
                # fmt: on

            elif command == "status":
                commands.status.run()

            elif command == "install":
                commands.install.run(prerelease=False)

            elif command == "install-prerelease":
                commands.install.run(prerelease=True)

            elif command == "rollback":
                commands.rollback.run()

            elif command == "remove":
                commands.remove.run()

            elif command == "exit":
                print("Exiting program")
                return

            else:
                utils.pretty_print(f'Unknown command "{command}"', color="red")

    except KeyboardInterrupt:
        utils.pretty_print("Exiting program")
    except Exception as e:
        utils.pretty_print("Exception occured!", color="red")
        raise e
