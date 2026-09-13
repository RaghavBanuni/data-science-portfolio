#!/usr/bin/env python3
"""Check that every project in ``projects.json`` is reachable and documented.

An index whose links have rotted is worse than no index, so the claim is checkable:

    python scripts/check_links.py            # HEAD each repository page
    python scripts/check_links.py --readme   # also require a non-trivial README

Standard library only, so it runs anywhere Python does. Network failures are reported as failures
rather than swallowed -- a checker that passes when the network is down checks nothing.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "projects.json"
TIMEOUT = 20
MIN_README_BYTES = 2000


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def fetch(url: str, method: str = "GET") -> tuple[int, bytes]:
    request = urllib.request.Request(
        url, method=method, headers={"User-Agent": "portfolio-link-check"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", action="store_true", help="also fetch and size each README")
    args = parser.parse_args(argv)

    registry = load_registry()
    owner = registry["owner"]
    failures: list[str] = []

    for project in registry["projects"]:
        slug = project["slug"]
        status, _ = fetch(f"https://github.com/{owner}/{slug}", method="HEAD")
        line = f"{slug:<44}{status}"

        if status != 200:
            failures.append(f"{slug}: repository returned {status}")
        elif args.readme:
            readme_status, body = fetch(
                f"https://raw.githubusercontent.com/{owner}/{slug}/main/README.md"
            )
            line += f"  README {readme_status} ({len(body)} bytes)"
            if readme_status != 200:
                failures.append(f"{slug}: README returned {readme_status}")
            elif len(body) < MIN_README_BYTES:
                failures.append(f"{slug}: README is only {len(body)} bytes")

        print(line)

    print(f"\n{len(registry['projects'])} projects checked, {len(failures)} problems")
    for failure in failures:
        print(f"  {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
