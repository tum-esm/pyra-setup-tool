import pytest
from src import tasks


@pytest.mark.order(3)
def test_check_python_version() -> None:
    tasks.check_environment.check_python_version()


@pytest.mark.order(3)
def test_check_command_availability() -> None:
    tasks.check_environment.check_command_availability("curl")
    tasks.check_environment.check_command_availability("tar")
    tasks.check_environment.check_command_availability("git")
