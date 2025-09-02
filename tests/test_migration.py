import pytest
import tum_esm_utils
import deepdiff
from src import Version, tasks

ALL_VERSIONS = [
    Version("4.0.5"),
    Version("4.0.6"),
    Version("4.0.7"),
    Version("4.0.8"),
    Version("4.1.0"),
    Version("4.1.1"),
    Version("4.1.2"),
    Version("4.1.3"),
    Version("4.1.4"),
    Version("4.2.0"),
    Version("4.2.1"),
    Version("4.2.2"),
    Version("4.2.3"),
    Version("4.2.4"),
]


@pytest.mark.order(2)
def test_migration() -> None:
    for variant in ["-minimal", "-full"]:
        for from_version in ALL_VERSIONS:
            src_config = tum_esm_utils.files.load_json_file(
                tum_esm_utils.files.rel_to_abs_path(
                    f"./configs/pyra-config-{from_version.tag[1:]}{variant}.json"
                )
            )
            for to_version in ALL_VERSIONS:
                if to_version <= from_version:
                    continue
                print(f"Testing migration from {from_version} to {to_version}")
                dst_config = tum_esm_utils.files.load_json_file(
                    tum_esm_utils.files.rel_to_abs_path(
                        f"./configs/pyra-config-{to_version.tag[1:]}{variant}.json"
                    )
                )
                migrated_src_config = tasks.migrate_config.migrate_config_object(
                    src_config, from_version, to_version
                )
                difference = deepdiff.DeepDiff(
                    migrated_src_config,
                    dst_config,
                    ignore_order=True,
                    ignore_numeric_type_changes=True,
                )
                assert len(difference) == 0, (
                    f"Migration from {from_version} to {to_version} failed."
                )
