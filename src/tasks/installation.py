import json
import os
import re
import shutil
import sys
from src.utils import directory_utils, migration_utils, printing_utils, shell_utils


def _install_python_dependencies(pyra_dir: str, version: str) -> None:
    code_dir = os.path.join(pyra_dir, f"pyra-{version}")

    """install system dependencies with poetry"""
    for command in [
        "poetry config virtualenvs.create false",
        "poetry env use system",
        "poetry install",
    ]:
        shell_utils.run_shell_command(command, cwd=code_dir, silent=False)
    printing_utils.pretty_print("Installed code dependencies", color="green")


def _run_ui_installer(pyra_dir: str, version: str) -> None:
    printing_utils.pretty_print(
        "Please install the UI using the installer that opens now", color="yellow"
    )
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version}_x64_en-US.msi"
    )
    try:
        shell_utils.run_shell_command(f"msiexec /i {ui_installer_path} /qf")
    except AssertionError:
        # ignore it when user cancels the installer window
        pass

    printing_utils.pretty_print("Installed the UI", color="green")


def _update_pyra_cli_pointer(pyra_dir: str, version: str) -> None:
    code_dir = os.path.join(pyra_dir, f"pyra-{version}")

    with open(os.path.join(pyra_dir, f"pyra-cli.bat"), "w") as f:
        pyra_cli_path = os.path.join(code_dir, "packages", "cli", "main.py")
        f.write("@echo off\n")
        f.write("echo.\n")
        f.write(f"python {pyra_cli_path} %*")
    printing_utils.pretty_print("Updated the link in pyra-cli.bat", color="green")


def _add_pyra_cli_to_env_path(pyra_dir: str) -> None:
    if pyra_cli_in_env_path():
        printing_utils.pretty_print(
            '"pyra-cli" command already in user environment variables', color="green"
        )
    else:
        printing_utils.pretty_input(
            f'Make the "pyra-cli" command available, by adding "{pyra_dir}" to '
            + f'your "user environment variables". See the pyra setup docs.',
            ["ok"],
        )


def _add_vscode_desktop_shortcut(pyra_dir: str, version: str) -> None:
    code_dir = os.path.join(pyra_dir, f"pyra-{version}")
    desktop_dir = directory_utils.get_desktop_dir()

    # Remove all old directory shortcuts
    p = re.compile("^open-pyra-\d+\.\d+\.\d+-directory\.bat$")
    old_shortcuts = [s for s in os.listdir(desktop_dir) if p.match(s) is not None]
    for s in old_shortcuts:
        os.remove(os.path.join(desktop_dir, s))

    # Create new shortcut for pyra-x.y.z directory. I used a ".bat"
    # script for this instead of a "windows shortcut" because the
    # latter are too much effort to create or require a python library
    with open(os.path.join(desktop_dir, f"open-pyra-{version}-directory.bat"), "w") as f:
        f.write(f"@ECHO OFF\nstart {code_dir}")

    printing_utils.pretty_print("Created desktop shortcut to code directory", color="green")


def install_version(version: str) -> None:
    """
    For a given release version "x.y.z", install
    the code and its ui-installer.
    """
    if sys.platform not in ["win32", "cygwin"]:
        print("Skipping installation on non-windows-platforms")
        return

    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")

    _install_python_dependencies(pyra_dir, version)
    _run_ui_installer(pyra_dir, version)
    _update_pyra_cli_pointer(pyra_dir, version)
    _add_pyra_cli_to_env_path(pyra_dir)
    _add_vscode_desktop_shortcut(pyra_dir, version)


def migrate_config(from_version: str, to_version: str) -> None:
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    src_path = os.path.join(pyra_dir, f"pyra-{from_version}", "config", "config.json")
    dst_path = os.path.join(pyra_dir, f"pyra-{to_version}", "config", "config.json")

    try:
        with open(src_path, "r") as f:
            old_config = json.load(f)

        # migrate from version n to n+1 to n+2 to ... until the final version is reached
        current_config, current_config_version = old_config, from_version
        while current_config_version != to_version:
            current_config, current_config_version = migration_utils.run(
                current_config, current_config_version
            )
        printing_utils.pretty_print(
            f"Migrated config from {from_version} to {to_version}", color="green"
        )
    except Exception as e:
        printing_utils.pretty_print(
            f'Could not migrate config. The config of version "{from_version}" '
            + f"might be invalid: {e}",
            color="red",
        )

    with open(dst_path, "w") as f:
        json.dump(current_config, f)


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


def pyra_cli_in_env_path() -> bool:
    pyra_dir = os.path.join(directory_utils.get_documents_dir(), "pyra")
    env_paths = shell_utils.run_shell_command(f"echo %PATH%").split(";")
    return pyra_dir in env_paths
