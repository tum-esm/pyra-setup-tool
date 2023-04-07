from src import tasks


def test_environment() -> None:
    tasks.check_environment.check_python_version()
    tasks.check_environment.check_command_availability("poetry")
    tasks.check_environment.check_command_availability("curl")
    tasks.check_environment.check_command_availability("tar")
    tasks.check_environment.check_command_availability("git")
