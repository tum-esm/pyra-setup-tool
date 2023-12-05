from src import Version, utils, tasks


def run() -> None:
    """Rolls back to a previous version of Pyra that was installed locally.

    This includes:
    - fetching the local pyra versions
    - asking the user which version should be rolled back to
    - switching to the selected version
    """

    local_pyra_versions = tasks.find_versions.get_local_versions()
    answer = utils.shell_utils.pretty_input(
        f"Which version should be rolled back to?",
        [v.as_str() for v in local_pyra_versions],
    )
    try:
        version_to_be_used = Version(answer)
    except AssertionError:
        utils.shell_utils.pretty_print(f'Invalid answer "{answer}"')
        return
    if version_to_be_used not in local_pyra_versions:
        utils.shell_utils.pretty_print(
            f'Invalid version "{version_to_be_used.as_str()}"'
        )
        return

    tasks.install_version.install_version(version_to_be_used)
    print("No migration, on rollbacks")

    utils.shell_utils.pretty_print("done!", color="green")
