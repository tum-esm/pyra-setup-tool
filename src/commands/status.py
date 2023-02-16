from src import tasks, utils


def run() -> None:
    local_pyra_versions = tasks.find_versions.get_local_versions()
    if len(local_pyra_versions) == 0:
        print("Did not find any local pyra versions.")
    else:
        print(f"Local pyra versions: {', '.join(local_pyra_versions)}")

    remote_pyra_versions = tasks.find_versions.get_remote_versions()
    if len(remote_pyra_versions) == 0:
        print("Did not find any remote pyra versions.")
    else:
        print(f"Remote pyra versions: {', '.join(remote_pyra_versions)}")

    print("Pyra CLI found in environment PATH variable: ", end="")
    if tasks.installation.pyra_cli_in_env_path():
        utils.printing_utils.pretty_print("Yes", color="green")
    else:
        utils.printing_utils.pretty_print("No", color="red")

    print("Pyra CLI is pointing to version: ", end="")
    cli_version = tasks.find_versions.get_version_used_in_cli()
    if cli_version is not None:
        utils.printing_utils.pretty_print(cli_version, color="green")
    else:
        utils.printing_utils.pretty_print("undefined", color="red")
