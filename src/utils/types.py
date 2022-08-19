from typing import TypedDict


class ReleaseDict(TypedDict):
    tag_name: str
    code_tarball_url: str
    ui_installer_url: str
