import json
from typing import Any


def run(from_dict: Any, from_version: str) -> tuple[Any, str]:
    try:
        to_version = {
            "4.0.4": "4.0.5",
            "4.0.5": "4.0.6",
            "4.0.6": "4.0.7",
        }[from_version]
    except KeyError:
        raise Exception(f'Unknown version "{from_version}"')

    to_dict = json.loads(json.dumps(from_dict))

    try:
        to_dict["general"]["version"] = to_version

        if to_version == "4.0.5":
            to_dict["measurement_triggers"]["consider_helios"] = to_dict[
                "measurement_triggers"
            ]["consider_vbdsd"]
            del to_dict["measurement_triggers"]["consider_vbdsd"]

            to_dict["helios"] = to_dict["vbdsd"]
            del to_dict["vbdsd"]

            if to_dict["helios"] is not None:
                to_dict["helios"]["edge_detection_threshold"] = 0.01

            to_dict["upload"] = None

        if to_version == "4.0.6":
            pass

        if to_version == "4.0.7":
            if to_dict["helios"] is not None:
                del to_dict["helios"]["measurement_threshold"]

        # add future migration rules here

    except Exception as e:
        raise Exception(
            f"Could not perform config migration " +
            f"{from_version} -> {to_version}: {e}"
        )

    return to_dict, to_version
