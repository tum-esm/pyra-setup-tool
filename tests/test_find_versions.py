import os
from src import utils, tasks, Version
from .fixtures import clear_local_pyra_dir


def test_get_local_versions(clear_local_pyra_dir: None) -> None:
    utils.initialize_pyra_directories()
    assert len(tasks.find_versions.get_local_versions()) == 0


def test_get_remote_versions() -> None:
    remote_versions = tasks.find_versions.get_remote_versions()
    assert len(remote_versions) >= 2
    assert Version("4.0.6") in remote_versions
    assert Version("4.0.7") in remote_versions
