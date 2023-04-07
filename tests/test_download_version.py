import os
from src import utils, tasks, Version
from .fixtures import clear_local_pyra_dir


def test_download_version(clear_local_pyra_dir: None) -> None:
    pyra_dir = os.path.join(utils.get_documents_dir(), "pyra")
    utils.initialize_pyra_directories()

    # TODO: do this for all found releases

    for v in ["4.0.6", "4.0.7"]:
        code_dir = os.path.join(pyra_dir, f"pyra-{v}")
        ui_installers_file = os.path.join(
            pyra_dir,
            "ui-installers",
            f"Pyra.UI_{v}_x64_en-US.msi",
        )

        assert not os.path.isdir(code_dir), f'directory "{code_dir}" should not exist'
        assert not os.path.isfile(
            ui_installers_file
        ), f'file "{ui_installers_file}" should not exist'
        assert v not in [lv.as_str() for lv in tasks.find_versions.get_local_versions()]

        tasks.download_version.download_version(Version(v))

        assert os.path.isdir(code_dir), f'directory "{code_dir}" should exist'
        assert os.path.isfile(ui_installers_file), f'file "{ui_installers_file}" should exist'
        assert v in [lv.as_str() for lv in tasks.find_versions.get_local_versions()]
