import subprocess

def run_tests():
    result = subprocess.run(['python', '-m', 'pytest', '-q'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Tests failed:")
        print(result.stderr)
    else:
        print("All tests passed.")

if __name__ == '__main__':
    run_tests()
