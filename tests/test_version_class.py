import pytest
from src import Version


@pytest.mark.order(2)
def test_version_class() -> None:
    v = Version("1.2.3")
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3
    assert v.as_str() == "1.2.3"
    assert v.as_tag() == "v1.2.3"
    assert v.as_ui_installer_name() == "Pyra.UI_1.2.3_x64_en-US.msi"
    assert v == Version("1.2.3")
    assert v != Version("1.2.4")
    assert v < Version("1.2.4")
    assert v < Version("1.3.0")
    assert v < Version("2.0.0")
    assert v > Version("1.2.2")
    assert v > Version("1.1.0")
    assert v > Version("0.0.0")
    assert v in [Version("1.2.3"), Version("1.2.4")]
    assert v in [Version("1.2.2"), Version("1.2.3")]
    assert v not in [Version("1.2.4"), Version("1.2.5")]

    assert Version("0.0.0") > Version("0.0.0-alpha.1")
    assert Version("1.0.0") > Version("1.0.0-alpha.1")
    assert Version("1.0.0") > Version("1.0.0-beta.1")
    assert Version("1.0.0-beta.1") > Version("1.0.0-alpha.1")
    assert Version("1.0.0-alpha.1") > Version("1.0.0-alpha.0")
    assert Version("1.0.0-alpha.10") > Version("1.0.0-alpha.2")
    assert Version("1.0.1-alpha.2") > Version("1.0.0")

    # check whether hashing works
    a = {  # pyright: ignore[reportUnusedVariable]
        Version("1.2.3"): 20,
        Version("1.2.4"): 30,
        Version("1.2.5"): 40,
        Version("1.2.3-beta.1"): 50,
        Version("1.2.3-alpha.1"): 50,
    }

    assert {
        Version("1.2.3"): 20,
        Version("1.2.4"): 30,
        Version("1.2.5"): 40,
    }[Version("1.2.4")] == 30
