import tum_esm_utils
import deepdiff
from src import Version, tasks


def test_migration() -> None:
    for from_version in [
        Version("4.0.5"),
        Version("4.0.6"),
        Version("4.0.7"),
        Version("4.0.8"),
        Version("4.1.0"),
    ]:
        src_config = tum_esm_utils.files.load_json_file(
            tum_esm_utils.files.rel_to_abs_path(
                f"./configs/pyra-config-{from_version.tag[1:]}.json"
            )
        )
        for to_version in [
            Version("4.0.6"),
            Version("4.0.7"),
            Version("4.0.8"),
            Version("4.1.0"),
            Version("4.1.1"),
        ]:
            if to_version <= from_version:
                continue
            print(f"Testing migration from {from_version} to {to_version}")
            dst_config = tum_esm_utils.files.load_json_file(
                tum_esm_utils.files.rel_to_abs_path(
                    f"./configs/pyra-config-{to_version.tag[1:]}.json"
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
            print(f"difference = {difference.to_json(indent=4)}")
            assert len(
                difference
            ) == 0, f"Migration from {from_version} to {to_version} failed."
