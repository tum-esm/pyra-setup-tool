import os
import shutil
from typing import Generator
import pytest
from src import utils


@pytest.fixture(scope="function")
def clear_local_pyra_dir() -> Generator[None, None, None]:
    pyra_dir = os.path.join(utils.get_documents_dir(), "pyra")

    if os.path.isdir(pyra_dir):
        shutil.rmtree(pyra_dir)

    yield

    if os.path.isdir(pyra_dir):
        shutil.rmtree(pyra_dir)
