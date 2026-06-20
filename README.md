# forge-ci-reliability

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI Status](https://img.shields.io/badge/CI-Pending-blue.svg)](https://github.com/Nueramarcos/forge-ci-reliability/actions)

Build reliability tooling: flaky test hunter, log parser, race condition detector. Isolates non-deterministic CI failures from chaotic build logs

## Usage

### Prerequisites
- Python 3.10+ (no installation required, run from the repository root)

### Examples

#### Build a project

```bash
python forge/cli.py build /path/to/rust/project
```

#### Build in release mode

```bash
python forge/cli.py build /path/to/project --release
```

#### Run a Python script

```bash
python forge/cli.py run script.py
```

#### Clean build artifacts

```bash
python forge/cli.py clean /path/to/project
python forge/cli.py clean . --all
```

## Usage Examples

### Build a Rust project
```bash
forge build /path/to/rust/project
```

### Build in release mode
```bash
forge build /path/to/project --release
```

### Run a Python script
```bash
forge run script.py
```

### Run a compiled binary
```bash
forge run /path/to/binary -- arg1 arg2
```

### Clean build artefacts
```bash
forge clean /path/to/project
```

### Clean including cache directories
```bash
forge clean /path/to/project --all
```
