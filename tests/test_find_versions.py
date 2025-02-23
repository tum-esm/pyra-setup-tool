import os

import pytest
from src import utils, tasks, Version
from .fixtures import clear_local_pyra_dir


@pytest.mark.order(3)
def test_get_local_versions(clear_local_pyra_dir: None) -> None:
    utils.initialize_pyra_directories()
    assert len(tasks.find_versions.get_local_versions()) == 0


@pytest.mark.order(3)
def test_get_remote_versions() -> None:
    remote_prerelease_versions = tasks.find_versions.get_remote_versions(prerelease=True)
    assert Version("4.0.5") in remote_prerelease_versions
    assert Version("4.0.6") not in remote_prerelease_versions

    remote_versions = tasks.find_versions.get_remote_versions()
    assert Version("4.0.5") not in remote_versions
    for v in ["4.0.6", "4.0.7", "4.0.8", "4.1.0", "4.1.1", "4.1.2", "4.1.3", "4.1.4", "4.2.0"]:
        assert Version(v) in remote_versions
