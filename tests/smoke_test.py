import subprocess
import sys


def test_cli_help():
    result = subprocess.run([sys.executable, "forge/cli.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage" in (result.stdout + result.stderr).lower()


def test_clean_command():
    result = subprocess.run([sys.executable, "forge/cli.py", "clean", "."], capture_output=True, text=True)
    assert result.returncode == 0
