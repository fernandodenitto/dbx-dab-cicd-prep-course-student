"""The generator's promises, as tests. Pure Python — no Spark, no workspace, seconds to run."""

import pytest

from lakeshore import datagen


@pytest.fixture(scope="module")
def data():
    return datagen.generate_all(seed=2026)


def test_same_seed_same_data(data):
    assert datagen.generate_all(seed=2026) == data


def test_different_seed_different_data(data):
    assert datagen.generate_all(seed=7)["customers"] != data["customers"]


def test_default_volumes(data):
    assert len(data["customers"]) == 200
    assert len(data["orders"]) == 1000
    assert len(data["products"]) == 20


def test_every_order_belongs_to_a_customer(data):
    customer_ids = {c["customer_id"] for c in data["customers"]}
    assert all(o["customer_id"] in customer_ids for o in data["orders"])


def test_orders_happen_after_signup(data):
    signup = {c["customer_id"]: c["created_at"] for c in data["customers"]}
    assert all(o["order_ts"] > signup[o["customer_id"]] for o in data["orders"])


def test_exactly_one_payment_per_order(data):
    assert sorted(p["order_id"] for p in data["payments"]) == sorted(
        o["order_id"] for o in data["orders"]
    )


def test_payment_amount_matches_items(data):
    orders = {o["order_id"]: o for o in data["orders"]}
    for p in data["payments"]:
        items = orders[p["order_id"]]["items"]
        assert p["amount"] == round(sum(i["quantity"] * i["unit_price"] for i in items), 2)


def test_refunds_only_completed_payments_and_never_exceed_them(data):
    payments = {p["payment_id"]: p for p in data["payments"]}
    for r in data["refunds"]:
        paid = payments[r["payment_id"]]
        assert paid["status_code"] == 1
        assert 0 < r["amount"] <= paid["amount"]


def test_clean_by_default(data):
    assert all(c["email"] for c in data["customers"])


def test_dirty_injects_null_emails_and_duplicates():
    dirty = datagen.generate_customers(n=200, seed=2026, dirty=True)
    assert any(c["email"] is None for c in dirty)
    assert len(dirty) > 200
