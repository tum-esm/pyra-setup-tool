from src import Version, utils, tasks


def run() -> None:
    """Rolls back to a previous version of Pyra that was installed locally.

    This includes:
    - fetching the local pyra versions
    - asking the user which version should be rolled back to
    - switching to the selected version
    """

    local_pyra_versions = tasks.find_versions.get_local_versions()
    if len(local_pyra_versions) == 0:
        print("Did not find any local pyra versions.")
        return

    while True:
        answer = utils.shell_utils.pretty_input(
            f"Which version should be rolled back to?",
            [v.as_str() for v in local_pyra_versions] + ["abort"],
        )
        if answer == "abort":
            utils.shell_utils.pretty_print("aborted by user")
            return
        try:
            version_to_be_used = Version(answer)
        except AssertionError:
            utils.shell_utils.pretty_print(f'Invalid answer "{answer}"')
            continue
        if version_to_be_used in local_pyra_versions:
            break
        else:
            utils.shell_utils.pretty_print(
                f'Invalid version "{version_to_be_used.as_str()}" (not installed locally)'
            )

    tasks.install_version.install_version(version_to_be_used)
    utils.shell_utils.pretty_print("No migration, on rollbacks")
    utils.shell_utils.pretty_print("done!", color="green")
