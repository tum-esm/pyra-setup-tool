import subprocess
from typing import Optional


def run_shell_command(command: str, cwd: Optional[str] = None) -> str:
    p = subprocess.run(
        command.split(" "),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )
    assert p.returncode == 0, (
        f"command '{command}' failed with exit code "
        + f"{p.returncode}: stderr = '{p.stderr.decode()}'"
    )
    return p.stdout.decode()
