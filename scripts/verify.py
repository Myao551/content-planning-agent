"""Run tests, then execute and export offline acceptance evidence."""
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from generate_examples import main as generate


def main():
    root = Path(__file__).resolve().parents[1]
    output = root / "examples"
    output.mkdir(exist_ok=True)
    start = time.monotonic()
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root, capture_output=True, text=True)
    stdout = result.stdout + result.stderr
    (output / "test-results.txt").write_text(stdout, encoding="utf-8")
    match = re.search(r"(\d+) passed", stdout)
    metadata = {"command": "python -m pytest -q", "exit_code": result.returncode,
                "passed_tests": int(match.group(1)) if match else None, "python": platform.python_version(),
                "recorded_at": datetime.now(timezone.utc).isoformat(), "wall_seconds": round(time.monotonic() - start, 6)}
    (output / "test-results.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(stdout, end="")
    if result.returncode:
        return result.returncode
    return generate()


if __name__ == "__main__":
    raise SystemExit(main())
