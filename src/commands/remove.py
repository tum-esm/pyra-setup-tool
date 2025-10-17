from src import Version, tasks, utils


def run() -> None:
    """Removes a local version of Pyra."""

    local_pyra_versions = tasks.find_versions.get_local_versions()
    if len(local_pyra_versions) == 0:
        print("Did not find any local pyra versions.")
        return

    while True:
        answer = utils.shell_utils.pretty_input(
            f"Which version should be removed?",
            [v.as_str() for v in local_pyra_versions] + ["abort"],
        )
        if answer == "abort":
            utils.shell_utils.pretty_print("aborted by user")
            return
        try:
            version_to_be_removed = Version(answer)
        except AssertionError:
            utils.shell_utils.pretty_print(f'Invalid answer "{answer}"')
            continue
        if version_to_be_removed in local_pyra_versions:
            break
        else:
            utils.shell_utils.pretty_print(
                f'Invalid version "{version_to_be_removed.as_str()}" (not installed locally)'
            )

    tasks.remove_version.remove_version(version_to_be_removed)
    utils.shell_utils.pretty_print("done!", color="green")
