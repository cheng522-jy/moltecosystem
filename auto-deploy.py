#!/usr/bin/env python3
import os
import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDE_DIRS = {".git", "node_modules"}
EXCLUDE_FILES = {"deploy.sh", "auto-deploy.py", "auto-deploy.sh"}
DEBOUNCE_SECONDS = 2.0
SLEEP_SECONDS = 1.0


def snapshot():
    entries = {}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        try:
            stat = path.stat()
        except FileNotFoundError:
            continue
        entries[str(path)] = (stat.st_mtime, stat.st_size)
    return entries


def run_deploy():
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    if status.returncode != 0:
        print("git status failed:", status.stderr.strip())
        return
    if not status.stdout.strip():
        return
    msg = f"auto: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["./deploy.sh", msg], cwd=ROOT)


def main():
    last = snapshot()
    pending = False
    last_change = 0.0

    print("Watching for changes. Press Ctrl+C to stop.")
    while True:
        time.sleep(SLEEP_SECONDS)
        current = snapshot()
        if current != last:
            pending = True
            last_change = time.time()
            last = current
        if pending and (time.time() - last_change) >= DEBOUNCE_SECONDS:
            run_deploy()
            pending = False


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
