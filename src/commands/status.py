from src import tasks, utils


def run() -> None:
    """Prints the status of the Pyra installation.

    This includes:
    - local pyra versions
    - remote pyra versions
    - whether the pyra-cli is in the environment PATH variable
    - which pyra version the pyra-cli is pointing to
    """

    local_pyra_versions = tasks.find_versions.get_local_versions()
    if len(local_pyra_versions) == 0:
        print("Did not find any local pyra versions.")
    else:
        print(
            f"Local pyra versions: {', '.join([v.as_str() for v in local_pyra_versions])}"
        )

    remote_pyra_versions = tasks.find_versions.get_remote_versions()
    if len(remote_pyra_versions) == 0:
        print("Did not find any remote pyra versions.")
    else:
        print(
            f"Remote pyra versions: {', '.join([v.as_str() for v in remote_pyra_versions])}"
        )

    pyra_cli_found_in_env_path = utils.pyra_dir_is_in_env_path()
    print("Pyra CLI found in environment PATH variable: ", end="")
    if pyra_cli_found_in_env_path:
        utils.shell_utils.pretty_print("Yes", color="green")
    else:
        utils.shell_utils.pretty_print("No", color="red")

    print("Pyra CLI is pointing to version: ", end="")
    cli_version = tasks.find_versions.get_version_used_in_cli()
    if cli_version is not None:
        utils.shell_utils.pretty_print(cli_version.as_str(), color="green")
    else:
        utils.shell_utils.pretty_print("undefined", color="red")
