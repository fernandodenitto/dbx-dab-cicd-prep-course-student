"""Land one batch of generated source files in a folder — locally or in a UC volume.

On Databricks the folder is a Unity Catalog volume path, /Volumes/<catalog>/<schema>/<volume>;
serverless compute exposes volumes as ordinary files, so plain `open()` works there and in tests.
"""

import argparse
from pathlib import Path

from lakeshore import datagen

# entity -> (file extension, writer)
FORMATS = {
    "customers": "json",
    "addresses": "tsv",
    "products": "csv",
    "orders": "json",
    "payments": "csv",
    "refunds": "csv",
}


def land_batch(root, batch=1, seed=datagen.DEFAULT_SEED, n_customers=200, n_orders=1000):
    """Generate every entity and write it under root/<entity>/; return {entity: path}."""
    data = datagen.generate_all(seed=seed, n_customers=n_customers, n_orders=n_orders)
    written = {}
    for entity, ext in FORMATS.items():
        folder = Path(root) / entity
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{entity}_batch_{batch:03d}.{ext}"
        if ext == "json":
            datagen.write_json(data[entity], path)
        else:
            datagen.write_csv(data[entity], path, delimiter="\t" if ext == "tsv" else ",")
        written[entity] = path
    return written


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Land a batch of Lakeshore source files.")
    parser.add_argument("--catalog", help="Unity Catalog catalog (with --schema and --volume)")
    parser.add_argument("--schema")
    parser.add_argument("--volume")
    parser.add_argument("--root", help="Write here instead of a volume (local runs, tests)")
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--seed", type=int, default=datagen.DEFAULT_SEED)
    args = parser.parse_args(argv)
    if not args.root and not (args.catalog and args.schema and args.volume):
        parser.error("give --root, or all of --catalog, --schema and --volume")
    return args


def main(argv=None):
    """Console entry point — the bundle's python_wheel_task calls this."""
    args = parse_args(argv)
    root = args.root or f"/Volumes/{args.catalog}/{args.schema}/{args.volume}"
    for entity, path in land_batch(root, batch=args.batch, seed=args.seed).items():
        print(f"{entity:<10} -> {path}")
