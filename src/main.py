import sys

try:
    import colorama
except ImportError:
    print('Please run "pip install colorama" first')
    sys.exit()

colorama.init()

from src.routines import (
    check_software_dependencies,
    find_versions,
    installation,
    manage_local_files,
)
from src.utils import directory_utils, printing_utils


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

        check_software_dependencies.check_python_version()
        check_software_dependencies.check_command_availability("poetry")
        check_software_dependencies.check_command_availability("tar")
        check_software_dependencies.check_command_availability("git")
        check_software_dependencies.check_command_availability("gh", name="github cli")
        check_software_dependencies.check_setup_tool_version()

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
                ["help", "status", "install", "remove", "exit"],
            )

            if command == "help":
                print("status:")
                print("    * list locally install versions")
                print("    * list available release version")
                print("    * show, if pyra-cli command is installed in environment path")
                print("    * show which pyra version the cli-command currently uses")
                print("install:")
                print("    * choose an available release version")
                print("    * download code from github")
                print("    * install dependencies")
                print("    * download UI and run windows installer")
                print("    * set the pyra-cli to point to the new version")
                print("    * test if pyra-cli command is installed in environment path")
                print("    * add desktop-shortcut to code directory")
                print("    * migrate config from an older version")
                print("remove:")
                print("    * remove a local version")
            if command == "status":
                local_pyra_versions = find_versions.get_local_versions()
                if len(local_pyra_versions) == 0:
                    print("Did not find any local pyra versions.")
                else:
                    print(f"Local pyra versions: {', '.join(local_pyra_versions)}")

                remote_pyra_versions = find_versions.get_remote_versions()
                if len(remote_pyra_versions) == 0:
                    print("Did not find any remote pyra versions.")
                else:
                    print(f"Remote pyra versions: {', '.join(remote_pyra_versions)}")

                print("Pyra CLI found in environment PATH variable: ", end="")
                if installation.pyra_cli_in_env_path():
                    printing_utils.pretty_print("Yes", color="green")
                else:
                    printing_utils.pretty_print("No", color="red")

                print("Pyra CLI is pointing to version: ", end="")
                cli_version = find_versions.get_version_used_in_cli()
                if cli_version is not None:
                    printing_utils.pretty_print(cli_version, color="green")
                else:
                    printing_utils.pretty_print("undefined", color="red")

            elif command == "install":
                local_pyra_versions = find_versions.get_local_versions()
                remote_pyra_versions = find_versions.get_remote_versions()
                if len(remote_pyra_versions) == 0:
                    print("Did not find any remote pyra versions.")
                    continue
                version_to_be_installed = printing_utils.pretty_input(
                    f"Which version should be installed?", remote_pyra_versions
                )
                if version_to_be_installed not in remote_pyra_versions:
                    printing_utils.pretty_print(f'Invalid version "{version_to_be_installed}"')
                    continue
                if version_to_be_installed in local_pyra_versions:
                    printing_utils.pretty_print(
                        f'Please uninstall the local "{version_to_be_installed}" first'
                    )
                    continue

                manage_local_files.download_version(version_to_be_installed)
                installation.install_version(version_to_be_installed)

                available_versions_to_migrate_from = (
                    find_versions.get_versions_to_migrate_from(version_to_be_installed)
                )
                if len(available_versions_to_migrate_from) == 0:
                    print("Skipping migration, no available versions to migrate from")
                else:
                    version_to_migrate_from = printing_utils.pretty_input(
                        f"Should we reuse the config.json from a previously installed version?",
                        [
                            "no",
                            *available_versions_to_migrate_from,
                        ],
                    )
                    if version_to_migrate_from != "no":
                        installation.migrate_config(
                            version_to_migrate_from, version_to_be_installed
                        )

                printing_utils.pretty_print("done!", color="green")

            elif command == "remove":
                local_pyra_versions = find_versions.get_local_versions()
                if len(local_pyra_versions) == 0:
                    print("Did not find any local pyra versions.")
                    continue
                version_to_be_removed = printing_utils.pretty_input(
                    f"Which version should be removed?", local_pyra_versions
                )
                if version_to_be_removed not in local_pyra_versions:
                    printing_utils.pretty_print(f'Invalid version "{version_to_be_removed}"')
                    continue

                manage_local_files.remove_version(version_to_be_removed)
                printing_utils.pretty_print("done!", color="green")

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
