import argparse
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.resolve()
FRONTEND_PATH = ROOT_PATH / "frontend"
BACKEND_PATH = ROOT_PATH / "backend"
BACKEND_DIST_PATH = BACKEND_PATH / "dist"
FRONTEND_DIST_PATH = FRONTEND_PATH / "dist"
ROOT_DIST_PATH = ROOT_PATH / "dist"
BACKEND_STATIC_PATH = BACKEND_PATH / "static"


def cprint(symbol: str, message: str, color: str = "34"):
    """Print with colored symbol prefix.

    Args:
        symbol: Single character symbol (i, >, !, +)
        message: Message to print
        color: ANSI color code (34=blue, 33=yellow, 32=green, 36=cyan)
    """
    print(f"\033[{color}m[{symbol}]\033[0m  {message}")


def safe_rmdir(path: Path):
    if path.exists():
        cprint(">", f"Removing: {path}")
        shutil.rmtree(path)


def safe_copy(src: Path, dst: Path):
    cprint(">", f"Copying {src} -> {dst}")
    shutil.copytree(str(src), str(dst))


def run(cmd, cwd, env=None):
    cprint(">", f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd, env=env)


def get_git_version() -> str:
    """Get version using git describe."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--always", "--dirty"],
            cwd=ROOT_PATH,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        cprint(
            "!",
            "Warning: Git version lookup failed, falling back to '0.0.0-unknown'",
            "33",
        )
        return "0.0.0-unknown"


def generate_metadata(version: str) -> Path:
    """Generate metadata.json for backend in a temporary location.

    Returns:
        Path to the generated metadata.json file
    """
    metadata = {
        "metadata-version": 1,
        "version": version,
    }

    # Use a fixed filename in temp directory (avoid random suffix from mkstemp)
    temp_dir = tempfile.mkdtemp(prefix="metadata_")
    temp_path = Path(temp_dir) / "metadata.json"

    cprint(">", f"Generating metadata: {temp_path}")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    cprint(">", f"Metadata content: {metadata}")

    return temp_path


def main():
    parser = argparse.ArgumentParser(description="Build script")
    parser.add_argument(
        "--version", type=str, help="Force build version (overrides git version)"
    )
    parser.add_argument(
        "--skip-frontend",
        action="store_true",
        help="Skip frontend build and static file update",
    )
    args = parser.parse_args()

    if args.version:
        version = args.version
        cprint(">", f"Using forced version: {version}")
    else:
        version = get_git_version()
        cprint(">", f"Using git version: {version}")

    skip_frontend = args.skip_frontend

    safe_rmdir(ROOT_DIST_PATH)
    safe_rmdir(FRONTEND_DIST_PATH)
    safe_rmdir(BACKEND_DIST_PATH)
    safe_rmdir(BACKEND_STATIC_PATH)

    # Frontend Build
    if skip_frontend:
        cprint(">", "Skipping frontend build...", "33")
    else:
        build_env = os.environ.copy()
        build_env["VITE_APP_VERSION"] = version
        build_env["VITE_APP_BUILD_TIME"] = datetime.now().isoformat()
        run(["pnpm", "build"], cwd=FRONTEND_PATH, env=build_env)

        # Update backend static
        safe_copy(FRONTEND_DIST_PATH, BACKEND_STATIC_PATH)
        safe_rmdir(FRONTEND_DIST_PATH)

    cprint(">", "Building backend...")
    metadata_path = generate_metadata(version)

    try:
        build_cmd = ["uv", "run", "--with", "pyinstaller", "pyinstaller", "-F", "-n", "EvATive7CloudImageHost"]
        if not skip_frontend:
            build_cmd.extend(
                [
                    "--add-data",
                    f"{BACKEND_STATIC_PATH}{os.pathsep}static",
                ]
            )
        build_cmd.extend(
            [
                "--add-data",
                f"{metadata_path}{os.pathsep}.",
            ]
        )
        build_cmd.append("./app.py")
        run(build_cmd, cwd=BACKEND_PATH)
    finally:
        # Clean up temporary metadata directory
        parent_dir = metadata_path.parent
        if parent_dir.exists():
            cprint(">", f"Cleaning up temporary metadata: {parent_dir}")
            shutil.rmtree(parent_dir)

    safe_copy(BACKEND_DIST_PATH, ROOT_DIST_PATH)
    safe_rmdir(BACKEND_DIST_PATH)

    cprint("+", "Build successful", "32")
    cprint("i", f"Avail at: {ROOT_DIST_PATH}", "36")


if __name__ == "__main__":
    main()
