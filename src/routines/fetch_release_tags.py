import json
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(PROJECT_DIR)
from src.utils import types, printing_utils


def fetch_release_tags() -> list[types.ReleaseDict]:
    credentials = os.environ.get("GITHUB_API_AUTH", None)
    if credentials is not None:
        printing_utils.pretty_print("Using GitHub authentication credentials")
        response = requests.get(
            "https://api.github.com/repos/tum-esm/pyra/releases",
            auth=HTTPBasicAuth(*credentials.split(":")),
        )
    else:
        response = requests.get("https://api.github.com/repos/tum-esm/pyra/releases")

    assert (
        response.status_code == 200
    ), f"API did not respond as expected: {response.text}"
    release_list = json.loads(response.text)
    results_list: list[types.ReleaseDict] = []
    if isinstance(release_list, list):
        for r in release_list:
            try:
                # release should have a msi file (microsoft installer file)
                assert len(r["assets"]) == 1
                assert r["tag_name"] >= "v4.0.4"
                assert r["assets"][0]["name"].endswith(".msi")
                results_list.append(
                    {
                        "tag_name": r["tag_name"],
                        "ui_installer_url": r["assets"][0]["browser_download_url"],
                        "commit_sha": r["target_commitish"],
                    }
                )
            except:
                pass
    return results_list


if __name__ == "__main__":
    print(fetch_release_tags())
