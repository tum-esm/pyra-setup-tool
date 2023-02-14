import subprocess
import os
from os.path import dirname

PROJECT_DIR = dirname(dirname(dirname(os.path.abspath(__file__))))

def run_shell_command(command: str, cwd: str = PROJECT_DIR, silent: bool = True) -> str:
    print(
        f'Running command "{command}"' + (f'" in directory {cwd}"' if cwd is not None else "")
    )
    if silent:
        p = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
        )
    else:
        p = subprocess.run(command, shell=True, cwd=cwd)

    if silent:
        try:
            stdout = p.stdout.decode("utf-8", errors="replace")
            stderr = p.stderr.decode("utf-8", errors="replace")
        except Exception as e:
            print(f"Error when decoding p: {p}")
            raise e
    else:
        stdout = "null"
        stderr = "null"

    assert p.returncode == 0, (
        f"command '{command}' failed with exit code " + f"{p.returncode}: stderr = '{stderr}'"
    )
    return stdout.strip()
