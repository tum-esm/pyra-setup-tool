from src import utils, tasks


def run() -> None:
    local_pyra_versions = tasks.find_versions.get_local_versions()
    remote_pyra_versions = tasks.find_versions.get_remote_versions()
    if len(remote_pyra_versions) == 0:
        print("Did not find any remote pyra versions.")
        return

    version_to_be_installed = utils.printing_utils.pretty_input(
        f"Which version should be installed?", remote_pyra_versions
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
    tasks.installation.install_version(version_to_be_installed)

    available_versions_to_migrate_from = tasks.find_versions.get_versions_to_migrate_from(
        version_to_be_installed
    )
    if len(available_versions_to_migrate_from) == 0:
        print("Skipping migration, no available versions to migrate from")
    else:
        version_to_migrate_from = utils.printing_utils.pretty_input(
            f"Should we reuse the config.json from a previously installed version?",
            [
                "no",
                *available_versions_to_migrate_from,
            ],
        )
        if version_to_migrate_from != "no":
            tasks.installation.migrate_config(version_to_migrate_from, version_to_be_installed)

    utils.printing_utils.pretty_print("done!", color="green")
