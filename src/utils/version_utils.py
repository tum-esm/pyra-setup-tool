import re
from typing import Literal


version_pattern = re.compile("^\d+\.\d+\.\d+$")


def version_difference(a: str, b: str) -> Literal[-1, 0, 1]:
    """
    Input: two versions "x.y.z"
    Output:
        * 1 if a < b
        * 0 if a == b
        * -1 if a > b
    """
    assert version_pattern.match(a)
    assert version_pattern.match(b)
    if a == b:
        return 0
    as_ = a.split(".")
    bs_ = b.split(".")
    if (int(as_[0]) * 1_000_000 + int(as_[1]) * 1_000 + int(as_[2])) < (
        int(bs_[0]) * 1_000_000 + int(bs_[1]) * 1_000 + int(bs_[2])
    ):
        return 1
    else:
        return -1
