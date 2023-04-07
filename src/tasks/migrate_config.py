import json
import os
import sys
from typing import Any
from src import Version, utils


def migrate_config(
    available_versions_to_migrate_from: list[Version], version: Version
) -> None:
    """Migrate the config.json from a previously installed version
    to the current version."""

    if len(available_versions_to_migrate_from) == 0:
        print("Skipping migration, no available versions to migrate from")
    else:
        version_to_migrate_from = utils.pretty_input(
            f"Should we reuse the config.json from a previously installed version?",
            [
                "no",
                *[v.as_str() for v in available_versions_to_migrate_from],
            ],
        )
        if version_to_migrate_from != "no":
            _migrate_config_files(Version(version_to_migrate_from), version)


def _migrate_config_files(from_version: Version, to_version: Version) -> None:
    pyra_dir = os.path.join(utils.get_documents_dir(), "pyra")
    src_path = os.path.join(pyra_dir, f"pyra-{from_version.as_str()}", "config", "config.json")
    dst_path = os.path.join(pyra_dir, f"pyra-{to_version.as_str()}", "config", "config.json")

    try:
        with open(src_path, "r") as f:
            old_config = json.load(f)

        # migrate from version n to n+1 to n+2 to ... until the final version is reached
        current_config, current_config_version = old_config, from_version
        while current_config_version != to_version:
            current_config, current_config_version = _migrate_a_single_config_object(
                current_config, current_config_version
            )
        utils.pretty_print(
            f"Migrated config from {from_version} to {to_version}", color="green"
        )
    except Exception as e:
        utils.pretty_print(
            f'Could not migrate config. The config of version "{from_version}" '
            + f"might be invalid: {e}",
            color="red",
        )

    with open(dst_path, "w") as f:
        json.dump(current_config, f)


def _migrate_a_single_config_object(
    from_dict: Any, from_version: Version
) -> tuple[Any, Version]:
    """Perform a config migration from one version to another.

    It accepts a config dict and a version string and returns
    the next config dict and version string.

    The migration works step by step, i.e. with `from_version`
    4.0.4 it will return the config for version 4.0.5."""

    try:
        to_version = {
            Version("v4.0.4"): Version("v4.0.5"),
            Version("v4.0.5"): Version("v4.0.6"),
            Version("v4.0.6"): Version("v4.0.7"),
        }[from_version]
    except KeyError:
        raise Exception(f'Unknown version "{from_version}"')

    to_dict = json.loads(json.dumps(from_dict))

    try:
        to_dict["general"]["version"] = to_version.as_str()

        if to_version == Version("v4.0.5"):
            to_dict["measurement_triggers"]["consider_helios"] = to_dict[
                "measurement_triggers"
            ]["consider_vbdsd"]
            del to_dict["measurement_triggers"]["consider_vbdsd"]

            to_dict["helios"] = to_dict["vbdsd"]
            del to_dict["vbdsd"]

            if to_dict["helios"] is not None:
                to_dict["helios"]["edge_detection_threshold"] = 0.01

            to_dict["upload"] = None

        if to_version == Version("v4.0.6"):
            pass

        if to_version == Version("v4.0.7"):
            if to_dict["helios"] is not None:
                del to_dict["helios"]["measurement_threshold"]

        # add future migration rules here

    except Exception as e:
        raise Exception(
            f"Could not perform config migration " + f"{from_version} -> {to_version}: {e}"
        )

    return to_dict, to_version
