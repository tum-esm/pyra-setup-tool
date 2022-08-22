import os
import sys


def _get_documents_dir() -> str:
    """
    The directory within which pyra will operate:

    📁 <documents directory>
        📁 pyra
            📁 ui-installers
            📁 pyra-x.y.z
            📁 pyra-x.y.z
            📁 ...
    """
    if sys.platform in ["darwin", "linux"]:
        documents_directory = os.environ["HOME"] + "/Documents"
    elif sys.platform in ["win32", "cygwin"]:
        documents_directory = os.environ["USERPROFILE"] + "\\Documents"
    else:
        raise Exception(f"Unknown platform '{sys.platform}'")

    assert os.path.isdir(
        documents_directory
    ), f"Documents directory does not exist. ({documents_directory})"

    return documents_directory


def initialize_pyra_directories() -> str:
    """
    Makes sure that PYRA's operatting directories exist.

    The directories within which pyra will operate:

    📁 <documents directory>
        📁 pyra
            📁 ui-installers
            📁 pyra-x.y.z
            📁 pyra-x.y.z
            📁 ...

    Returns the path to documents/pyra
    """
    documents_directory = _get_documents_dir()

    pyra_directory = os.path.join(documents_directory, "pyra")
    ui_installers_directory = os.path.join(documents_directory, "pyra", "ui-installers")
    if not os.path.isdir(pyra_directory):
        os.mkdir(pyra_directory)
        print(f"Created directory '{pyra_directory}'")

    if not os.path.isdir(ui_installers_directory):
        os.mkdir(ui_installers_directory)
        print(f"Created directory '{ui_installers_directory}'")

    return pyra_directory


def get_local_pyra_versions() -> list[str]:
    """Returns a list ["4.0.1", "4.0.2", ...] of pyra versions installed locally"""
    pyra_directory = os.path.join(_get_documents_dir(), "pyra")

    return [
        d[5:]
        for d in os.listdir(pyra_directory)
        if (d.startswith("pyra-") and os.path.isdir(os.path.join(pyra_directory, d)))
    ]
