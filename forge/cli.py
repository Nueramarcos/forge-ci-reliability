"""
Forge - CLI
Argument parser with cmd_build wired to a real build system dispatcher.
"""

import argparse
import subprocess
import shutil
import sys
import textwrap
import time
from pathlib import Path
from typing import Callable

__version__ = "0.2.0"


# ── Command registry ──────────────────────────────────────────────────────────

_COMMANDS: dict[str, Callable[[argparse.Namespace], int]] = {}


def command(name: str):
    def decorator(fn: Callable[[argparse.Namespace], int]):
        _COMMANDS[name] = fn
        return fn
    return decorator


# ── Build system detection ────────────────────────────────────────────────────

def _detect_build_system(target: Path) -> str | None:
    """
    Inspect the target directory and return the build system to use,
    or None if we can't determine one.
    """
    markers = {
        "Cargo.toml":    "cargo",
        "pyproject.toml": "python",
        "setup.py":      "python",
        "package.json":  "npm",
        "Makefile":      "make",
        "CMakeLists.txt": "cmake",
        "build.gradle":  "gradle",
        "pom.xml":       "mvn",
    }
    for filename, system in markers.items():
        if (target / filename).exists():
            return system
    return None


# ── Build system runners ──────────────────────────────────────────────────────

def _run_cargo(target: Path, release: bool, jobs: int, verbose: bool) -> int:
    cmd = ["cargo", "build"]
    if release:
        cmd.append("--release")
    cmd += ["--jobs", str(jobs)]
    if verbose:
        cmd.append("--verbose")
    return _exec(cmd, cwd=target)


def _run_python(target: Path, release: bool, jobs: int, verbose: bool) -> int:
    # Try pip install -e . (editable install covers both setup.py and pyproject.toml)
    cmd = [sys.executable, "-m", "pip", "install", "-e", str(target)]
    if not verbose:
        cmd.append("-q")
    return _exec(cmd)


def _run_npm(target: Path, release: bool, jobs: int, verbose: bool) -> int:
    install = _exec(["npm", "install"], cwd=target)
    if install != 0:
        return install
    script = "build:prod" if release else "build"
    # gracefully fall back if the script doesn't exist
    result = subprocess.run(
        ["npm", "run", script, "--if-present"],
        cwd=target,
    )
    return result.returncode


def _run_make(target: Path, release: bool, jobs: int, verbose: bool) -> int:
    cmd = ["make", f"-j{jobs}"]
    if release:
        cmd.append("RELEASE=1")
    if verbose:
        cmd.append("V=1")
    return _exec(cmd, cwd=target)


def _run_cmake(target: Path, release: bool, jobs: int, verbose: bool) -> int:
    build_dir = target / ("build_release" if release else "build_debug")
    build_dir.mkdir(exist_ok=True)
    build_type = "Release" if release else "Debug"
    configure = _exec(
        ["cmake", "..", f"-DCMAKE_BUILD_TYPE={build_type}"],
        cwd=build_dir,
    )
    if configure != 0:
        return configure
    return _exec(["cmake", "--build", ".", f"-j{jobs}"], cwd=build_dir)


_RUNNERS: dict[str, Callable[[Path, bool, int, bool], int]] = {
    "cargo":  _run_cargo,
    "python": _run_python,
    "npm":    _run_npm,
    "make":   _run_make,
    "cmake":  _run_cmake,
}


# ── Shell helper ──────────────────────────────────────────────────────────────

def _exec(cmd: list[str], cwd: Path | None = None) -> int:
    """Run a command, stream output, and return the exit code."""
    display = " ".join(cmd)
    print(f"  $ {display}")
    t0 = time.perf_counter()
    try:
        result = subprocess.run(cmd, cwd=cwd)
        elapsed = time.perf_counter() - t0
        status = "✓" if result.returncode == 0 else "✗"
        print(f"  {status} exited {result.returncode} in {elapsed:.2f}s")
        return result.returncode
    except FileNotFoundError:
        tool = cmd[0]
        print(f"  ✗ {tool!r} not found — is it installed and on PATH?")
        return 127


def _tool_available(tool: str) -> bool:
    return shutil.which(tool) is not None


# ── Subcommands ───────────────────────────────────────────────────────────────

@command("build")
def cmd_build(args: argparse.Namespace) -> int:
    if args.version:
        print(__version__)
        return 0

    target = Path(args.target).resolve()

    if not target.exists():
        print(f"[build] error: target path does not exist: {target}")
        return 1

    system = args.system or _detect_build_system(target)

    if system is None:
        print(
            f"[build] error: could not detect a build system under {target}\n"
            f"  Supported: {', '.join(_RUNNERS)}\n"
            f"  Use --system <name> to specify one explicitly."
        )
        return 1

    runner = _RUNNERS.get(system)
    if runner is None:
        print(f"[build] error: unsupported build system {system!r}")
        return 1

    print(
        f"[build] target={args.target!r}  system={system}  "
        f"release={args.release}  jobs={args.jobs}"
    )
    return runner(target, args.release, args.jobs, args.verbose)


@command("run")
def cmd_run(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    extra = args.args or []

    if not target.exists():
        print(f"[run] error: {target} does not exist")
        return 1

    # Try to infer how to run based on file extension / build system
    system = _detect_build_system(target) if target.is_dir() else None

    if target.suffix == ".py" or (system == "python"):
        cmd = [sys.executable, str(target)] + extra
    elif target.suffix in (".sh", ""):
        cmd = [str(target)] + extra
    elif system == "cargo":
        cmd = ["cargo", "run", "--manifest-path", str(target / "Cargo.toml")] + (
            ["--release"] if args.release else []
        ) + (["--"] if extra else []) + extra
    elif system == "npm":
        cmd = ["npm", "run", "start", "--prefix", str(target)] + extra
    else:
        print(f"[run] error: don't know how to run {args.target!r}")
        return 1

    print(f"[run] target={args.target!r}  extra={extra!r}")
    return _exec(cmd)


@command("clean")
def cmd_clean(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    print(f"[clean] target={args.target!r}  all={args.all}")

    system = _detect_build_system(target)

    if system == "cargo":
        return _exec(["cargo", "clean", "--manifest-path", str(target / "Cargo.toml")])
    if system == "npm":
        return _exec(["npm", "run", "clean", "--if-present", "--prefix", str(target)])
    if system == "cmake":
        for d in (target / "build_debug", target / "build_release"):
            if d.exists():
                import shutil as _sh
                _sh.rmtree(d)
                print(f"  removed {d}")
        return 0

    # Generic: remove common artifact dirs
    dirs = ["dist", "build", "__pycache__", ".pytest_cache", "target"]
    if args.all:
        dirs += [".mypy_cache", ".ruff_cache", "node_modules"]

    removed = 0
    for name in dirs:
        p = target / name
        if p.exists():
            import shutil as _sh
            _sh.rmtree(p)
            print(f"  removed {p}")
            removed += 1

    print(f"  cleaned {removed} artifact(s)")
    return 0


# ── Parser factory ────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Forge – project build & run tool
            ─────────────────────────────────
            Auto-detects: cargo · python · npm · make · cmake
        """),
    )
    parser.add_argument("--version", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # build
    p_build = sub.add_parser("build", help="compile / build a target")
    p_build.add_argument("target", help="path to project root")
    p_build.add_argument("--release", action="store_true")
    p_build.add_argument("-j", "--jobs", type=int, default=4, metavar="N")
    p_build.add_argument(
        "--system",
        choices=list(_RUNNERS),
        default=None,
        help="override auto-detected build system",
    )

    # run
    p_run = sub.add_parser("run", help="run a built target")
    p_run.add_argument("target")
    p_run.add_argument("--release", action="store_true")
    p_run.add_argument("args", nargs=argparse.REMAINDER)

    # clean
    p_clean = sub.add_parser("clean", help="remove build artifacts")
    p_clean.add_argument("target", nargs="?", default=".")
    p_clean.add_argument("--all", action="store_true")

    return parser


# ── Entry point ───────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verbose:
        print(f"[forge] verbose  command={args.command!r}")
    handler = _COMMANDS.get(args.command)
    if handler is None:
        parser.error(f"unknown command: {args.command!r}")
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
