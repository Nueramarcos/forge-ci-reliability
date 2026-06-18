# Contributing to forge-ci-reliability

## Python 3.10+ Setup

Ensure you have Python 3.10 or later installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Nueramarcos/forge-ci-reliability.git
   cd forge-ci-reliability
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the forge CLI

To run the forge CLI, follow these steps:

1. Ensure you are in the root directory of the repository.
2. Run the desired command:
   ```sh
   python forge/cli.py <command> <project_path>
   ```

For example:
- To build a project:
  ```sh
  python forge/cli.py build /path/to/project
  ```
- To run a project:
  ```sh
  python forge/cli.py run /path/to/project
  ```
- To clean a project:
  ```sh
  python forge/cli.py clean /path/to/project
  ```

## Contribution Guidelines

1. **Fork the Repository**: Fork this repository to your GitHub account.
2. **Create a New Branch**: Create a new branch for your feature or bug fix.
   ```sh
   git checkout -b feature/my-feature
   ```
3. **Make Changes**: Make your changes and commit them with descriptive messages.
   ```sh
   git add .
   git commit -m "Add my feature"
   ```
4. **Push to Your Fork**: Push your changes to your forked repository.
   ```sh
   git push origin feature/my-feature
   ```
5. **Create a Pull Request**: Go to the original repository and create a pull request from your fork.

By following these guidelines, you can help ensure that your contributions are integrated smoothly into the project.
