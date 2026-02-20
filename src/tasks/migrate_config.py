import json
import os
from typing import Any
from src import Version, utils


def migrate_config(available_versions_to_migrate_from: list[Version], version: Version) -> None:
    """Migrate the config.json from a previously installed version
    to the current version."""

    if len(available_versions_to_migrate_from) == 0:
        print("Skipping migration, no available versions to migrate from")
    else:
        answer = utils.pretty_input(
            f"Should we reuse the config.json from a previously installed version?",
            [
                "no",
                *[v.as_str() for v in available_versions_to_migrate_from],
            ],
        )
        if answer != "no":
            try:
                version_to_migrate_from = Version(answer)
            except AssertionError:
                utils.pretty_print(f'Invalid answer "{answer}"')
                return
            _migrate_config_files(version_to_migrate_from, version)


def _migrate_config_files(from_version: Version, to_version: Version) -> None:
    pyra_dir = os.path.join(utils.get_documents_dir(), "pyra")
    src_path = os.path.join(pyra_dir, f"pyra-{from_version.as_str()}", "config", "config.json")
    dst_path = os.path.join(pyra_dir, f"pyra-{to_version.as_str()}", "config", "config.json")

    try:
        with open(src_path, "r") as f:
            old_config = json.load(f)

        # migrate from version n to n+1 to n+2 to ... until the final version is reached
        new_config = migrate_config_object(old_config, from_version, to_version)
        utils.pretty_print(
            f"Migrated config from {from_version.as_str()} to {to_version.as_str()}",
            color="green",
        )

        with open(dst_path, "w") as f:
            json.dump(new_config, f)
    except Exception as e:
        utils.pretty_print(
            f'Could not migrate config. The config of version "{from_version.as_str()}" '
            + f"might be invalid: {e}",
            color="red",
        )


def migrate_config_object(
    from_config_dict: Any,
    from_version: Version,
    to_version: Version,
) -> Any:
    current_config, current_config_version = from_config_dict, from_version
    while current_config_version != to_version:
        current_config, current_config_version = _migrate_a_single_config_object(
            current_config, current_config_version
        )
    return current_config


def _migrate_a_single_config_object(from_dict: Any, from_version: Version) -> tuple[Any, Version]:
    """Perform a config migration from one version to another.

    It accepts a config dict and a version string and returns
    the next config dict and version string.

    The migration works step by step, i.e. with `from_version`
    4.0.4 it will return the config for version 4.0.5."""

    try:
        to_version = {
            Version("v4.0.5"): Version("v4.0.6"),
            Version("v4.0.6"): Version("v4.0.7"),
            Version("v4.0.7"): Version("v4.0.8"),
            Version("v4.0.8"): Version("v4.1.0"),
            Version("v4.1.0"): Version("v4.1.1"),
            Version("v4.1.1"): Version("v4.1.2"),
            Version("v4.1.2"): Version("v4.1.3"),
            Version("v4.1.3"): Version("v4.1.4"),
            Version("v4.1.4"): Version("v4.2.0"),
            Version("v4.2.0"): Version("v4.2.1"),
            Version("v4.2.1"): Version("v4.2.2"),
            Version("v4.2.2"): Version("v4.2.3"),
            Version("v4.2.3"): Version("v4.2.4"),
            Version("v4.2.4"): Version("v4.2.5"),
            Version("v4.2.5"): Version("v4.2.6"),
            Version("v4.2.6"): Version("v4.2.7"),
            Version("v4.2.7"): Version("v5.0.0-beta.1"),
            Version("v5.0.0-beta.1"): Version("v5.0.0-beta.2"),
        }[from_version]
    except KeyError:
        raise Exception(f'Unknown version "{from_version.as_str()}"')

    to_dict: dict[Any, Any] = json.loads(json.dumps(from_dict))
    assert isinstance(to_dict, dict), f"config is not a dictionary, got {to_dict}"

    try:
        to_dict["general"]["version"] = to_version.as_str()

        if to_version == Version("v4.0.6"):
            if (
                to_dict["error_email"]["sender_password"] == "..."
                and to_dict["error_email"]["sender_address"] == "pyra.technical.user@gmail.com"
            ):
                to_dict["error_email"]["sender_address"] = "technical-user@domain.com"

        if to_version == Version("v4.0.7"):
            if to_dict["helios"] is not None:
                del to_dict["helios"]["measurement_threshold"]

        if to_version == Version("v4.0.8"):
            to_dict["camtracker"]["motor_offset_threshold"] = abs(
                to_dict["camtracker"]["motor_offset_threshold"]
            )

        if to_version == Version("v4.1.0"):
            # camtracker
            to_dict["camtracker"]["restart_if_logs_are_too_old"] = False
            to_dict["camtracker"]["restart_if_cover_remains_closed"] = False

            # error emails
            to_dict["error_email"]["smtp_host"] = "smtp.gmail.com"
            to_dict["error_email"]["smtp_port"] = 587
            to_dict["error_email"]["smtp_username"] = from_dict["error_email"]["sender_address"]
            to_dict["error_email"]["smtp_password"] = from_dict["error_email"]["sender_password"]
            del to_dict["error_email"]["sender_password"]

            # helios
            if to_dict.get("helios", None) is not None:
                to_dict["helios"]["min_seconds_between_state_changes"] = 180
                to_dict["helios"]["edge_pixel_threshold"] = (
                    from_dict["helios"]["edge_detection_threshold"] * 100
                )
                del to_dict["helios"]["edge_detection_threshold"]
                to_dict["helios"]["edge_color_threshold"] = 40
                to_dict["helios"]["target_pixel_brightness"] = 50
                to_dict["helios"]["save_images_to_archive"] = from_dict["helios"]["save_images"]
                del to_dict["helios"]["save_images"]
                to_dict["helios"]["save_current_image"] = False

            # upload
            if to_dict.get("upload", None) is not None:
                del to_dict["upload"]["upload_ifgs"]
                del to_dict["upload"]["src_directory_ifgs"]
                del to_dict["upload"]["dst_directory_ifgs"]
                del to_dict["upload"]["remove_src_ifgs_after_upload"]
                del to_dict["upload"]["upload_helios"]
                del to_dict["upload"]["dst_directory_helios"]
                del to_dict["upload"]["remove_src_helios_after_upload"]
                to_dict["upload"]["streams"] = [
                    {
                        "is_active": from_dict["upload"]["upload_ifgs"],
                        "label": "interferograms",
                        "variant": "directories",
                        "dated_regex": "^%Y%m%d$",
                        "src_directory": from_dict["upload"]["src_directory_ifgs"],
                        "dst_directory": from_dict["upload"]["dst_directory_ifgs"],
                        "remove_src_after_upload": from_dict["upload"][
                            "remove_src_ifgs_after_upload"
                        ],
                    },
                    {
                        "is_active": False,
                        "label": "datalogger",
                        "variant": "files",
                        "dated_regex": "^datalogger-%Y-%m-%d*$",
                        "src_directory": "...",
                        "dst_directory": "...",
                        "remove_src_after_upload": False,
                    },
                ]

        if to_version == Version("v4.1.1"):
            if to_dict.get("upload", None) is not None:
                to_dict["upload"]["only_upload_at_night"] = True

        if to_version == Version("v4.1.2"):
            pass

        if to_version == Version("v4.1.3"):
            if to_dict.get("upload", None) is not None:
                to_dict["upload"]["only_upload_when_not_measuring"] = True

        if to_version == Version("v4.1.4"):
            pass

        if to_version == Version("v4.2.0"):
            to_dict["opus"]["automatic_peak_positioning"] = False
            to_dict["opus"]["interferogram_path"] = ""
            to_dict["measurement_triggers"]["shutdown_grace_period"] = 300

            to_dict["tum_enclosure"] = json.loads(json.dumps(to_dict["tum_plc"]))
            del to_dict["tum_plc"]

            to_dict["general"]["seconds_per_core_iteration"] = to_dict["general"][
                "seconds_per_core_interval"
            ]
            del to_dict["general"]["seconds_per_core_interval"]

        if to_version == Version("v4.2.1"):
            if to_dict["general"]["min_sun_elevation"] == 11:
                to_dict["general"]["min_sun_elevation"] = 5
            to_dict["opus"]["automatic_peak_positioning_dcmin"] = 0.02
            to_dict["camtracker"]["working_directory_path"] = "\\".join(
                str(to_dict["camtracker"]["executable_path"]).replace("/", "\\").split("\\")[:-1]
            )
            if to_dict["upload"] is not None:
                to_dict["upload"]["is_active"] = True

        if to_version == Version("v4.2.2"):
            pass

        if to_version == Version("v4.2.3"):
            pass

        if to_version == Version("v4.2.4"):
            if to_dict["helios"] is not None:
                to_dict["helios"]["camera_brightness"] = 64
                to_dict["helios"]["camera_contrast"] = 64

        if to_version == Version("v4.2.5"):
            pass

        if to_version == Version("v4.2.6"):
            pass

        if to_version == Version("v4.2.7"):
            pass

        if to_version == Version("v5.0.0-beta.1"):
            to_dict["aemet_enclosure"] = None

        if to_version == Version("v5.0.0-beta.2"):
            pass

        # add future migration rules here

    except Exception as e:
        raise Exception(
            f"Could not perform config migration "
            + f"{from_version.as_str()} -> {to_version.as_str()}: {repr(e)}"
        )

    return to_dict, to_version
