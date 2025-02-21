import os
from src import utils, tasks
from .fixtures import clear_local_pyra_dir


def test_download_version(clear_local_pyra_dir: None) -> None:
    pyra_dir = os.path.join(utils.get_documents_dir(), "pyra")
    utils.initialize_pyra_directories()

    for v in tasks.find_versions.get_remote_versions():
        code_dir = os.path.join(pyra_dir, f"pyra-{v.as_str()}")
        ui_installers_file = os.path.join(
            pyra_dir,
            "ui-installers",
            v.as_ui_installer_name(),
        )

        assert not os.path.isdir(code_dir), f'directory "{code_dir}" should not exist'
        assert not os.path.isfile(ui_installers_file), (
            f'file "{ui_installers_file}" should not exist'
        )
        assert v not in tasks.find_versions.get_local_versions()

        tasks.download_version.download_version(v)

        assert os.path.isdir(code_dir), f'directory "{code_dir}" should exist'
        assert os.path.isfile(ui_installers_file), f'file "{ui_installers_file}" should exist'
        assert v in tasks.find_versions.get_local_versions()
