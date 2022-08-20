import os
import sys

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(PROJECT_DIR)
from src.utils import get_documents_dir, printing_utils, run_shell_command


def download_release_assets(release_tag: str) -> None:
    credentials = os.environ.get("GITHUB_API_AUTH", None)
    documents_dir = get_documents_dir.get_documents_dir()
    pyra_dir = os.path.join(documents_dir, "pyra")

    tar_name = f"pyra-{release_tag[1:]}.tar.gz"
    ui_installer_name = f"Pyra.UI_{release_tag[1:]}_x64_en-US.msi"

    if credentials is not None:
        printing_utils.pretty_print("Using GitHub authentication credentials")

    # download codebase tarball
    run_shell_command.run_shell_command(
        f"gh release download --repo tum-esm/pyra --archive=tar.gz {release_tag}",
        cwd=pyra_dir,
    )
    # download ui installer
    run_shell_command.run_shell_command(
        f"gh release download --repo tum-esm/pyra {release_tag}",
        cwd=pyra_dir,
    )

    # extract code from tarball
    run_shell_command.run_shell_command(f"tar -xf {tar_name}", cwd=pyra_dir)

    # remove tarball file
    run_shell_command.run_shell_command(f"rm {tar_name}", cwd=pyra_dir)

    # move ui installer
    os.rename(
        os.path.join(pyra_dir, ui_installer_name),
        os.path.join(pyra_dir, "ui-installer", ui_installer_name),
    )

    # open the eplorer at that location using 'explorer ...' (windows) and 'open ...' (unix)


if __name__ == "__main__":
    download_release_assets("v4.0.4")
