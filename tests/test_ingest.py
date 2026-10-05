"""The ingest entry point, run against a temporary folder instead of a UC volume."""

import csv
import json

import pytest

from lakeshore import ingest


def test_land_batch_writes_every_entity(tmp_path):
    written = ingest.land_batch(tmp_path, batch=3)
    assert set(written) == set(ingest.FORMATS)
    assert written["orders"].name == "orders_batch_003.json"
    first_order = json.loads(written["orders"].read_text().splitlines()[0])
    assert first_order["items"]  # nested array survives the round trip


def test_tsv_and_csv_have_headers(tmp_path):
    written = ingest.land_batch(tmp_path)
    with written["addresses"].open() as f:
        assert next(csv.reader(f, delimiter="\t"))[0] == "customer_id"
    with written["payments"].open() as f:
        assert "status_code" in next(csv.reader(f))


def test_main_with_root(tmp_path, capsys):
    ingest.main(["--root", str(tmp_path), "--batch", "2"])
    assert (tmp_path / "refunds" / "refunds_batch_002.csv").exists()
    assert "orders" in capsys.readouterr().out


def test_volume_path_is_built_from_catalog_schema_volume():
    args = ingest.parse_args(["--catalog", "c", "--schema", "s", "--volume", "v"])
    assert (args.catalog, args.schema, args.volume) == ("c", "s", "v")


def test_missing_destination_is_an_error():
    with pytest.raises(SystemExit):
        ingest.parse_args(["--catalog", "only_this"])
