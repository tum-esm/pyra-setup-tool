from src.utils import shell_utils


def fetch_release_tags() -> list[str]:
    result = shell_utils.run_shell_command("gh release list --repo tum-esm/pyra")
    releases = [
        r.replace("\t", " ").split(" ")[0]
        for r in result.stdout.decode().split("\n")
        if r != ""
    ]
    return releases
