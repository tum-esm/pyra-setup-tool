import os
import re
import shutil
from src.utils import directory_utils, shell_utils


def install_version(version: str) -> None:
    """
    For a given release version "x.y.z", install
    the code and its ui-installer.
    """
    desktop_dir = directory_utils.get_desktop_dir()
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    code_dir = os.path.join(pyra_dir, f"pyra-{version}")

    # Install system dependencies with poetry
    for command in [
        "poetry config virtualenvs.create false",
        "poetry env use system",
        "poetry install",
    ]:
        shell_utils.run_shell_command(command, cwd=code_dir)

    # Run UI installer
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version}_x64_en-US.msi"
    )
    shell_utils.run_shell_command(f"msiexec /i {ui_installer_path} /qf")

    # Update "pyra-cli.bat" file
    with open(os.path.join(pyra_dir, f"pyra-cli.bat"), "w") as f:
        pyra_cli_path = os.path.join(code_dir, "packages", "cli", "main.py")
        f.write(f"@echo off\necho.\npython {pyra_cli_path} %")

    # Remove all old directory shortcuts
    p = re.compile("^open-pyra-\d+\.\d+\.\d+-directory\.bat$")
    old_shortcuts = [s for s in os.listdir(desktop_dir) if p.match(s) is not None]
    for s in old_shortcuts:
        os.remove(os.path.join(desktop_dir, s))

    # Create new shortcut for pyra-x.y.z directory. I used a ".bat"
    # script for this instead of a "windows shortcut" because the
    # latter are too much effort to create or require a python library
    with open(
        os.path.join(desktop_dir, f"open-pyra-{version}-directory.bat"), "w"
    ) as f:
        f.write(f"@ECHO OFF\nstart {code_dir}")


# TODO
def migrate_config(from_version: str, to_version: str) -> None:
    pass


def remove_version(version: str) -> None:
    """
    For a given release version "x.y.z", remove
    the code and its ui-installer.
    """
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version}_x64_en-US.msi"
    )
    code_dir = os.path.join(pyra_dir, f"pyra-{version}")

    if os.path.isdir(code_dir):
        shutil.rmtree(code_dir)

    if os.path.isfile(ui_installer_path):
        os.remove(ui_installer_path)
