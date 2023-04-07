from src import tasks, utils


def run() -> None:
    """Removes a local version of Pyra."""

    local_pyra_versions = tasks.find_versions.get_local_versions()
    if len(local_pyra_versions) == 0:
        print("Did not find any local pyra versions.")
        return
    version_to_be_removed = utils.printing_utils.pretty_input(
        f"Which version should be removed?", local_pyra_versions
    )
    if version_to_be_removed not in local_pyra_versions:
        utils.printing_utils.pretty_print(f'Invalid version "{version_to_be_removed}"')
        return

    tasks.manage_local_files.remove_version(version_to_be_removed)
    utils.printing_utils.pretty_print("done!", color="green")
