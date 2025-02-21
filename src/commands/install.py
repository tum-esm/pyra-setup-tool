from src import Version, utils, tasks


def run(prerelease: bool = False) -> None:
    """Installs a new version of Pyra.

    This includes:
    - fetching the remote pyra versions
    - asking the user which version should be installed
    - downloading the selected version
    - switching to the selected version (install dependencies, switch CLI pointer)
    - migrating the config.json between version
    """

    local_pyra_versions = tasks.find_versions.get_local_versions()
    remote_pyra_versions = tasks.find_versions.get_remote_versions(prerelease=prerelease)
    if len(remote_pyra_versions) == 0:
        print("Did not find any remote pyra versions.")
        return

    answer = utils.shell_utils.pretty_input(
        f"Which version should be installed?",
        [v.as_str() for v in remote_pyra_versions],
    )
    try:
        version_to_be_installed = Version(answer)
    except AssertionError:
        utils.shell_utils.pretty_print(f'Invalid answer "{answer}"')
        return

    if version_to_be_installed not in remote_pyra_versions:
        utils.shell_utils.pretty_print(f'Invalid version "{version_to_be_installed.as_str()}"')
        return

    if version_to_be_installed in local_pyra_versions:
        utils.shell_utils.pretty_print(
            f'Please remove the local version "{version_to_be_installed.as_str()}" first'
        )
        return

    tasks.download_version.download_version(version_to_be_installed)
    tasks.install_version.install_version(version_to_be_installed)

    # migrate the config.json between version
    available_versions_to_migrate_from = tasks.find_versions.get_versions_to_migrate_from(
        version_to_be_installed
    )
    tasks.migrate_config.migrate_config(available_versions_to_migrate_from, version_to_be_installed)

    utils.shell_utils.pretty_print("done!", color="green")
