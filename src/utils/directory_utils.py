import os
import sys

from .shell_utils import run_shell_command


def get_documents_dir() -> str:
    """The directory within which pyra will operate:

    ```
    📁 <documents directory>
        📁 pyra
            📁 ui-installers
            📁 pyra-x.y.z
            📁 pyra-x.y.z
            📁 ...
    ```
    """

    if sys.platform in ["darwin", "linux"]:
        documents_directory = os.environ["HOME"] + "/Documents"
    elif sys.platform in ["win32", "cygwin"]:
        documents_directory = os.environ["USERPROFILE"] + "\\Documents"
    else:
        raise Exception(f"Unknown platform '{sys.platform}'")

    assert os.path.isdir(documents_directory), (
        f"Documents directory does not exist. ({documents_directory})"
    )

    return documents_directory


def get_desktop_dir() -> str:
    """The directory where shortcuts should be placed."""

    if sys.platform in ["darwin", "linux"]:
        desktop_directory = os.environ["HOME"] + "/Desktop"
    elif sys.platform in ["win32", "cygwin"]:
        desktop_directory = os.environ["USERPROFILE"] + "\\Desktop"
    else:
        raise Exception(f"Unknown platform '{sys.platform}'")

    assert os.path.isdir(desktop_directory), (
        f"Desktop directory does not exist. ({desktop_directory})"
    )

    return desktop_directory


def initialize_pyra_directories() -> str:
    """Makes sure that PYRA's operating directories exist.

    The directories within which pyra will operate:

    ```
    📁 <documents directory>
        📁 pyra
            📁 ui-installers
            📁 pyra-x.y.z
            📁 pyra-x.y.z
            📁 ...
    ```

    Returns the path to `.../pyra`.
    """

    docs_directory = get_documents_dir()

    pyra_directory = os.path.join(docs_directory, "pyra")
    ui_installers_directory = os.path.join(docs_directory, "pyra", "ui-installers")
    if not os.path.isdir(pyra_directory):
        os.mkdir(pyra_directory)
        print(f"Created directory '{pyra_directory}'")

    if not os.path.isdir(ui_installers_directory):
        os.mkdir(ui_installers_directory)
        print(f"Created directory '{ui_installers_directory}'")

    return pyra_directory


def pyra_dir_is_in_env_path() -> bool:
    """Checks if the pyra directory is in the environment's
    PATH variable."""

    pyra_dir = os.path.join(get_documents_dir(), "pyra")
    env_paths = run_shell_command(f"echo %PATH%").split(";")
    return pyra_dir in env_paths
