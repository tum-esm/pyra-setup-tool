
from src import Version

def test_migration() -> None:
    for from_version in [
        Version("4.0.5"),
        Version("4.0.6"),
        Version("4.0.7"),
        Version("4.0.8")
    ]:
        pass