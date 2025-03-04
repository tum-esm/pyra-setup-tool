import os
import re
import shutil
import sys
from src import Version, utils

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS_DIR = os.path.join(SRC_DIR, "utils", "requirements")


def install_version(version: Version) -> None:
    """For a given release version "x.y.z" installed locally, switch to that version.

    This includes
    * install python dependencies
    * run UI installer
    * update pyra-cli pointer
    * check whether pyra-cli is in env paths
    * create VS Code desktop shortcut to code directory
    """

    if sys.platform not in ["win32", "cygwin"]:
        print("Skipping installation on non-windows-platforms")
        return

    pyra_dir = os.path.join(utils.get_documents_dir(), "pyra")

    _uninstall_current_python_dependencies(pyra_dir, version)
    _install_new_python_dependencies(pyra_dir, version)
    _run_ui_installer(pyra_dir, version)
    _update_pyra_cli_pointer(pyra_dir, version)
    _add_pyra_cli_to_env_path(pyra_dir)
    _add_pyra_dir_desktop_shortcut(pyra_dir, version)


def _uninstall_current_python_dependencies(pyra_dir: str, version: Version) -> None:
    """install system dependencies with pip"""

    code_dir = os.path.join(pyra_dir, f"pyra-{version.as_str()}")
    out = utils.run_shell_command("pip freeze", cwd=code_dir, silent=True)
    installed_packages: list[str] = []
    for line in out.split("\n"):
        if "==" in line:
            package_name = line.split("==")[0]
            installed_packages.append(package_name)
        elif " @ " in line:
            package_name = line.split(" @ ")[0]
            installed_packages.append(package_name)
    if "pip" in installed_packages:
        installed_packages.remove("pip")
    utils.run_shell_command(
        f"pip uninstall -y {' '.join(installed_packages)}", cwd=code_dir, silent=False
    )


def _install_new_python_dependencies(pyra_dir: str, version: Version) -> None:
    """install system dependencies with pip"""

    code_dir = os.path.join(pyra_dir, f"pyra-{version.as_str()}")
    if version <= Version("4.1.2"):
        requirements_src_path = os.path.join(REQUIREMENTS_DIR, f"{version.as_str()}.txt")
        requirements_dst_path = os.path.join(code_dir, "requirements.txt")
        if not os.path.isfile(requirements_dst_path):
            assert os.path.isfile(requirements_src_path), f"File not found: {requirements_src_path}"
            shutil.copyfile(requirements_src_path, requirements_dst_path)

        utils.run_shell_command("pip install -r requirements.txt", cwd=code_dir, silent=False)
    else:
        utils.run_shell_command("pip install .", cwd=code_dir, silent=False)
    utils.pretty_print("Installed code dependencies", color="green")


def _run_ui_installer(pyra_dir: str, version: Version) -> None:
    """Runs the UI installer (`.msi`) which opens another window the user
    has to click through."""

    utils.pretty_print("Please install the UI using the installer that opens now", color="yellow")
    ui_installer_path = os.path.join(
        pyra_dir, "ui-installers", f"Pyra.UI_{version.as_str()}_x64_en-US.msi"
    )
    try:
        utils.run_shell_command(f"msiexec /i {ui_installer_path} /qf")
    except AssertionError:
        # ignore it when user cancels the installer window
        pass

    utils.pretty_print("Installed the UI", color="green")


def _update_pyra_cli_pointer(pyra_dir: str, version: Version) -> None:
    """Updates the pyra-cli.bat file to point to the new version of the CLI."""

    code_dir = os.path.join(pyra_dir, f"pyra-{version.as_str()}")

    with open(os.path.join(pyra_dir, f"pyra-cli.bat"), "w") as f:
        pyra_cli_path = os.path.join(code_dir, "packages", "cli", "main.py")
        f.write("@echo off\n")
        f.write("echo.\n")
        f.write(f"python {pyra_cli_path} %*")
    utils.pretty_print("Updated the link in pyra-cli.bat", color="green")


def _add_pyra_cli_to_env_path(pyra_dir: str) -> None:
    """Print instriuctions to add the pyra-cli command to the user
    environment variables if it is not already there."""

    if utils.pyra_dir_is_in_env_path():
        utils.pretty_print(
            '"pyra-cli" command already in user environment variables', color="green"
        )
    else:
        utils.pretty_input(
            f'Make the "pyra-cli" command available, by adding "{pyra_dir}" to '
            + f'your "user environment variables". See the pyra setup docs.',
            ["ok"],
        )


def _add_pyra_dir_desktop_shortcut(pyra_dir: str, version: Version) -> None:
    """Adds a desktop shortcut to open the pyra dir in the file explorer."""

    code_dir = os.path.join(pyra_dir, f"pyra-{version.as_str()}")
    desktop_dir = utils.get_desktop_dir()

    # Remove all old directory shortcuts
    p = re.compile(r"^open-pyra-\d+\.\d+\.\d+-directory\.bat$")
    old_shortcuts = [s for s in os.listdir(desktop_dir) if p.match(s) is not None]
    for s in old_shortcuts:
        os.remove(os.path.join(desktop_dir, s))

    # Create new shortcut for pyra-x.y.z directory. I used a ".bat"
    # script for this instead of a "windows shortcut" because the
    # latter are too much effort to create or require a python library
    with open(os.path.join(desktop_dir, f"open-pyra-{version.as_str()}-directory.bat"), "w") as f:
        f.write(f"@ECHO OFF\nstart {code_dir}")

    utils.pretty_print("Created desktop shortcut to code directory", color="green")
