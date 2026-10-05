"""Read `databricks bundle plan -o json` output — for humans (summary) and for gates (compare).

    python scripts/plan_report.py summary plan.json [title]       # markdown for PRs / summaries
    python scripts/plan_report.py compare approved.json new.json  # exit 1 if actions differ
    python scripts/plan_report.py drift plan.json                 # exit 1 on remote drift

"compare" looks at WHAT happens to WHICH resource (create / update / delete / recreate),
not at field values: a new wheel timestamp or a new commit tag is expected between two
plans, a new delete is not.
"""

import json
import sys

# Field changes that are expected on every deploy and carry no review value.
NOISE = ("tags['git_commit']", "spec.dependencies")


def load(path):
    with open(path) as f:
        return json.load(f)["plan"]


def actions(plan):
    return {key: entry["action"] for key, entry in plan.items() if entry["action"] != "skip"}


def changed_fields(entry):
    changes = entry.get("changes") or {}
    return [
        field
        for field, change in changes.items()
        if change.get("action") != "skip" and not any(n in field for n in NOISE)
    ]


def summary(path, title="Bundle plan"):
    plan = load(path)
    rows = actions(plan)
    lines = [f"### {title}", ""]
    if not rows:
        return "\n".join(lines + ["No changes."])
    lines += ["| Resource | Action | Fields |", "|---|---|---|"]
    for key, action in sorted(rows.items()):
        fields = ", ".join(f"`{f}`" for f in changed_fields(plan[key])) or "—"
        marker = " ⚠️" if action in ("delete", "recreate") else ""
        lines.append(f"| `{key}` | **{action}**{marker} | {fields} |")
    return "\n".join(lines)


def compare(approved_path, fresh_path):
    approved, fresh = actions(load(approved_path)), actions(load(fresh_path))
    if approved == fresh:
        print("Plans match: the deploy will do what was approved.")
        return 0
    for key in sorted(set(approved) | set(fresh)):
        if approved.get(key) != fresh.get(key):
            print(f"MISMATCH {key}: approved={approved.get(key)} now={fresh.get(key)}")
    return 1


def drift(path):
    """Fields whose value in the workspace differs from what was last deployed.

    Planned changes (new wheel, new commit tag) have old != new but remote == old: not drift.
    Someone editing the workspace makes remote != old: drift. Fields the plan marks "skip"
    (server-side defaults, IDs, timestamps) are ignored.
    """
    found = []
    for key, entry in load(path).items():
        for field, change in (entry.get("changes") or {}).items():
            # "skip" entries are fields the server fills in (defaults, IDs, timestamps).
            if change.get("action") == "skip" or "remote" not in change:
                continue
            if change.get("remote") != change.get("old"):
                found.append((key, field, change.get("old"), change.get("remote")))
    for key, field, old, remote in found:
        print(f"DRIFT {key} {field}: deployed={old!r} workspace={remote!r}")
    if not found:
        print("No drift: the workspace matches the last deployment.")
    return 1 if found else 0


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["summary"] and len(args) >= 2:
        print(summary(args[1], *args[2:3]))
        return 0
    if args[:1] == ["compare"] and len(args) == 3:
        return compare(args[1], args[2])
    if args[:1] == ["drift"] and len(args) == 2:
        return drift(args[1])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
