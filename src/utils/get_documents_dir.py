import os
import sys


def get_documents_dir() -> str:
    """
    The directory where pyra will operate

    📁 <documents directory>
        📁 pyra
            📁 pyra-x.y.z
    """
    if sys.platform in ["darwin", "linux"]:
        return os.environ["HOME"] + "/Documents"
    elif sys.platform in ["win32", "cygwin"]:
        return os.environ["USERPROFILE"] + "\\Documents"
    else:
        raise Exception(f"Unknown platform '{sys.platform}'")
