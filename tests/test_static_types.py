import os
import tum_esm_utils

PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


def _rm(path: str) -> None:
    os.system(f"rm -rf {os.path.join(PROJECT_DIR, path)}")


def test_static_types() -> None:
    _rm(".mypy_cache/3.10/src")
    _rm(".mypy_cache/3.10/tests")
    _rm(".mypy_cache/3.10/run.*")

    for path in ["run.py", "src/", "tests/"]:
        assert os.system(f"cd {PROJECT_DIR} && python -m mypy {path}") == 0
