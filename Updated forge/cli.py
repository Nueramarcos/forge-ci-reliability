import sys

def build(project_path):
    print(f"Building project at {project_path}")
    # Add actual build logic here

def clean(project_path):
    print(f"Cleaning project at {project_path}")
    # Add actual clean logic here

def run(project_path):
    print(f"Running project at {project_path}")
    # Add actual run logic here

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python forge/cli.py <command> <project_path>")
        sys.exit(1)

    command = sys.argv[1]
    project_path = sys.argv[2]

    if command == 'build':
        build(project_path)
    elif command == 'clean':
        clean(project_path)
    elif command == 'run':
        run(project_path)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
