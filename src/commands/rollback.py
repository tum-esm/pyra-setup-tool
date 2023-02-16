from src import utils, tasks


def run() -> None:
    local_pyra_versions = tasks.find_versions.get_local_versions()
    version_to_be_used = utils.printing_utils.pretty_input(
        f"Which version should be rolled back to?", local_pyra_versions
    )
    if version_to_be_used not in local_pyra_versions:
        utils.printing_utils.pretty_print(f'Invalid version "{version_to_be_used}"')
        return

    tasks.installation.switch_to_pyra_version(version_to_be_used)
    print("No migration, on rollbacks")

    utils.printing_utils.pretty_print("done!", color="green")
