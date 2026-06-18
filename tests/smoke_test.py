import subprocess

def test_build_command():
    result = subprocess.run(['python', 'forge/cli.py', 'build', '.'], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Build successful" in result.stdout

def test_clean_command():
    result = subprocess.run(['python', 'forge/cli.py', 'clean', '.'], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Clean successful" in result.stdout

def test_run_command():
    result = subprocess.run(['python', 'forge/cli.py', 'run', '.'], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Run successful" in result.stdout
