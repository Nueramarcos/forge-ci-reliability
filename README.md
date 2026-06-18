# forge-ci-reliability
Build reliability tooling: flaky test hunter, log parser, race condition detector. Isolates non-deterministic CI failures from chaotic build logs

## Usage

### Prerequisites
- Python 3.10+ (no installation required, run from the repository root)

### Examples

#### Build a project

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
