import os

import pytest
from src import utils
from .fixtures import clear_local_pyra_dir


@pytest.mark.order(3)
def test_get_documents_dir() -> None:
    d = utils.get_documents_dir()
    assert d.endswith("Documents")
    assert d == os.path.expanduser("~/Documents")
    assert os.path.isdir(d)


@pytest.mark.order(3)
def test_get_desktop_dir() -> None:
    d = utils.get_desktop_dir()
    assert d.endswith("Desktop")
    assert d == os.path.expanduser("~/Desktop")
    assert os.path.isdir(d)


@pytest.mark.order(3)
def test_initialize_pyra_directories(clear_local_pyra_dir: None) -> None:
    pyra_dir = os.path.join(os.path.abspath(utils.get_documents_dir()), "pyra")
    ui_installers_dir = os.path.join(pyra_dir, "ui-installers")
    assert not os.path.isdir(pyra_dir), f'directory "{pyra_dir}" should not exist'

    assert utils.initialize_pyra_directories() == pyra_dir

    assert os.path.isdir(pyra_dir), f'directory "{pyra_dir}" should exist'
    assert os.path.isdir(ui_installers_dir), f'directory "{ui_installers_dir}" should exist'


@pytest.mark.order(3)
def test_pyra_dir_is_in_env_path() -> None:
    utils.pyra_dir_is_in_env_path()
