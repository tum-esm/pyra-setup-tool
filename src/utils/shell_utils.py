import subprocess
from typing import Optional


def run_shell_command(command: str, cwd: Optional[str] = None) -> str:
    p = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )
    try:
        stdout = p.stdout.decode("utf-8", errors="replace")
        stderr = p.stderr.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error when decoding p: {p}")
        raise e

    assert p.returncode == 0, (
        f"command '{command}' failed with exit code " + f"{p.returncode}: stderr = '{stderr}'"
    )
    return stdout
