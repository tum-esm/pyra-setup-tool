import subprocess


def run_shell_command(command: str, cwd: str = None) -> str:
    print(command)
    p = subprocess.run(
        command.split(" "),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )
    assert p.returncode == 0, (
        f"command '{command}' failed with exit code "
        + f"{p.returncode}: stderr = '{p.stderr}'"
    )
    return p.stdout.decode()
