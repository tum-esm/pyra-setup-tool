import os
import sys
import pytest
import tum_esm_utils

PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


def _rm(path: str) -> None:
    os.system(f"rm -rf {os.path.join(PROJECT_DIR, path)}")


@pytest.mark.order(1)
def test_with_mypy() -> None:
    _rm(".mypy_cache/3.10/src")
    _rm(".mypy_cache/3.10/tests")
    _rm(".mypy_cache/3.10/run.*")

    for path in ["run.py", "src/", "tests/"]:
        assert os.system(f"cd {PROJECT_DIR} && {sys.executable} -m mypy {path}") == 0


@pytest.mark.order(1)
def test_with_pyright() -> None:
    os.environ["TUM_ESM_UTILS_EXPLICIT_IMPORTS"] = "1"
    assert os.system(f"cd {PROJECT_DIR} && {sys.executable} -m pyright") == 0
