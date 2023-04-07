from src import Version, utils, tasks


def run() -> None:
    """Rolls back to a previous version of Pyra that was installed locally.

    This includes:
    - fetching the local pyra versions
    - asking the user which version should be rolled back to
    - switching to the selected version
    """

    local_pyra_versions = tasks.find_versions.get_local_versions()
    version_to_be_used = Version(
        utils.printing_utils.pretty_input(
            f"Which version should be rolled back to?",
            [v.as_str() for v in local_pyra_versions],
        )
    )
    if version_to_be_used not in local_pyra_versions:
        utils.printing_utils.pretty_print(f'Invalid version "{version_to_be_used}"')
        return

    tasks.installation.switch_to_pyra_version(version_to_be_used)
    print("No migration, on rollbacks")

    utils.printing_utils.pretty_print("done!", color="green")
