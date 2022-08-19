import json
from . import types
import requests


def fetch_release_tags() -> list[types.ReleaseDict]:
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
                        "code_tarball_url": r["tarball_url"],
                        "ui_installer_url": r["assets"][0]["browser_download_url"],
                    }
                )
            except:
                pass
    return results_list


if __name__ == "__main__":
    print(fetch_release_tags())
