"""Fail if a dashboard in the repo pins a catalog or schema.

`databricks bundle generate dashboard` writes the catalog and schema it found in the
workspace (your dev ones) into every dataset. Committed, they would make staging and
prod read dev data: the bundle's dataset_catalog / dataset_schema only fill in what the
file leaves empty. Run with --fix to strip them.
"""

import json
import sys
from pathlib import Path

PINNED = ("catalog", "schema")


def check(path, fix=False):
    dashboard = json.loads(path.read_text())
    problems = []
    for dataset in dashboard.get("datasets", []):
        for key in PINNED:
            if key in dataset:
                problems.append(f"{path}: dataset '{dataset['name']}' pins {key}={dataset[key]!r}")
                if fix:
                    del dataset[key]
    if fix and problems:
        path.write_text(json.dumps(dashboard, indent=2) + "\n")
    return problems


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    fix = "--fix" in args
    problems = [p for f in sorted(Path("src").rglob("*.lvdash.json")) for p in check(f, fix)]
    for p in problems:
        print(("fixed: " if fix else "") + p)
    return 0 if fix or not problems else 1


if __name__ == "__main__":
    sys.exit(main())
