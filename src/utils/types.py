from typing import TypedDict


class ReleaseDict(TypedDict):
    tag_name: str
    ui_installer_url: str
    commit_sha: str
