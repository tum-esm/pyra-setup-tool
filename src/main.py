import sys
from src.routines import check_software_dependencies, find_versions, manage_local_files
from src.utils import directory_utils, printing_utils


def run():
    try:
        printing_utils.print_line()
        printing_utils.pretty_print(
            "Welcome to the pyra-setup-tool! Instruction formatting: "
        )
        printing_utils.pretty_print("  * checkpoints = green ", color="green")
        printing_utils.pretty_print(
            "  * expecting user input = yellow ", color="yellow"
        )
        printing_utils.print_line()

        # the following check is necessary because I did not manage
        # to (possibly) deactivate the current venv from within
        # a subprocess/system call, etc.
        printing_utils.pretty_print(
            "Please DO NOT use a virtual environment for PYRA! Use the"
            + " system interpreter available via the command 'python'. "
            + f"Currently using the interpreter '{sys.executable}'"
        )
        printing_utils.pretty_print(
            f"Run 'which python' in another shell. Are system-"
            + "interpreter and the current one identical? (Y/n) ",
            color="yellow",
            end="",
        )
        if not input().startswith("Y"):
            printing_utils.pretty_print("Aborting", color="red")
            return

        check_software_dependencies.check_python_version()
        check_software_dependencies.check_poetry_availability()
        check_software_dependencies.check_tar_availability()
        check_software_dependencies.check_github_cli_availability()

        pyra_directory = directory_utils.initialize_pyra_directories()
        printing_utils.pretty_print(
            f'Successfully initialized local environment inside "{pyra_directory}"',
            color="green",
        )

        # now we can assume that the required system state is present
        # (software dependencies and code/ui directories)

        # Infinite loop (select from install|uninstall|abort)
        while True:
            printing_utils.print_line()
            printing_utils.pretty_print(
                "Enter a command (list-local | list-remote | install | remove | exit) ",
                color="yellow",
                end="",
            )
            command = input("").strip()

            if command == "list-local":
                local_pyra_versions = find_versions.get_local_versions()
                if len(local_pyra_versions) == 0:
                    print("Did not find any local pyra versions.")
                else:
                    print(f"Local pyra versions: {', '.join(local_pyra_versions)}")

            elif command == "list-remote":
                remote_pyra_versions = find_versions.get_remote_versions()
                if len(remote_pyra_versions) == 0:
                    print("Did not find any remote pyra versions.")
                else:
                    print(f"Remote pyra versions: {', '.join(remote_pyra_versions)}")

            elif command == "install":
                pass

            elif command == "remove":
                local_pyra_versions = find_versions.get_local_versions()
                if len(local_pyra_versions) == 0:
                    print("Did not find any local pyra versions.")
                    continue
                printing_utils.pretty_print(
                    f"Which version should be removed? ({' | '.join(local_pyra_versions)}) ",
                    color="yellow",
                    end="",
                )
                version_to_be_removed = input("")
                if version_to_be_removed not in local_pyra_versions:
                    printing_utils.pretty_print(
                        f'Invalid version "{version_to_be_removed}"'
                    )
                    continue

                manage_local_files.remove_release(f"v{version_to_be_removed}")
                printing_utils.pretty_print("done!")

            elif command == "exit":
                print("Exiting program")
                return

            else:
                printing_utils.pretty_print(f'Unknown command "{command}"', color="red")

    except Exception as e:
        printing_utils.pretty_print("Exception occured!", color="red")
        raise e
