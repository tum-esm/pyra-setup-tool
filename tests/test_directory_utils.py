import os
from src import utils


def test_get_documents_dir() -> None:
    assert os.path.abspath(utils.get_documents_dir()).endswith("Documents")


def test_get_desktop_dir() -> None:
    assert os.path.abspath(utils.get_desktop_dir()).endswith("Desktop")


def test_initialize_pyra_directories() -> None:
    pyra_dir = utils.initialize_pyra_directories()
    assert os.path.isdir(pyra_dir)
    assert os.path.isdir(os.path.join(pyra_dir, "ui-installers"))


def test_pyra_dir_is_in_env_path() -> None:
    utils.pyra_dir_is_in_env_path()
