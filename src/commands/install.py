from src import Version, utils, tasks


def run() -> None:
    """Installs a new version of Pyra.

    This includes:
    - fetching the remote pyra versions
    - asking the user which version should be installed
    - downloading the selected version
    - switching to the selected version (install dependencies, switch CLI pointer)
    - migrating the config.json between version
    """

    local_pyra_versions = tasks.find_versions.get_local_versions()
    remote_pyra_versions = tasks.find_versions.get_remote_versions()
    if len(remote_pyra_versions) == 0:
        print("Did not find any remote pyra versions.")
        return

    version_to_be_installed = Version(
        utils.printing_utils.pretty_input(
            f"Which version should be installed?",
            [v.as_str() for v in remote_pyra_versions],
        )
    )
    if version_to_be_installed not in remote_pyra_versions:
        utils.printing_utils.pretty_print(f'Invalid version "{version_to_be_installed}"')
        return

    if version_to_be_installed in local_pyra_versions:
        utils.printing_utils.pretty_print(
            f'Please uninstall the local "{version_to_be_installed}" first'
        )
        return

    tasks.manage_local_files.download_version(version_to_be_installed)
    tasks.installation.switch_to_pyra_version(version_to_be_installed)

    # migrate the config.json between version
    available_versions_to_migrate_from = tasks.find_versions.get_versions_to_migrate_from(
        version_to_be_installed
    )
    tasks.installation.perform_migration(
        available_versions_to_migrate_from, version_to_be_installed
    )

    utils.printing_utils.pretty_print("done!", color="green")
