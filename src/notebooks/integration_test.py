# Databricks notebook source
# MAGIC %md
# MAGIC # Integration test
# MAGIC
# MAGIC Runs in staging after every deploy, against the real environment: the objects the
# MAGIC bundle created, the data the daily job produced, the contract downstream users rely
# MAGIC on (gold columns and types). Unit tests can't see any of this.

# COMMAND ----------

dbutils.widgets.text("catalog", "lakeshore_staging")
dbutils.widgets.text("landing_schema", "landing")
dbutils.widgets.text("gold_schema", "gold")
catalog = dbutils.widgets.get("catalog")
landing = dbutils.widgets.get("landing_schema")
gold = f"{catalog}.{dbutils.widgets.get('gold_schema')}"
failures = []


def check(condition, message):
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        failures.append(message)


# COMMAND ----------

# 1. The landing volume exists and holds a file for every entity.
entities = {f.name.rstrip("/") for f in dbutils.fs.ls(f"/Volumes/{catalog}/{landing}/files")}
expected = {"customers", "addresses", "products", "orders", "payments", "refunds"}
check(expected <= entities, f"landing volume has folders for {sorted(expected)}")

# 2. The gold contract: these columns, these types. Dashboards depend on it.
schema = {f.name: f.dataType.simpleString() for f in spark.table(f"{gold}.orders_by_day").schema}
check(schema.get("order_date") == "date", f"orders_by_day.order_date is date ({schema})")
check(schema.get("n_orders") == "bigint", "orders_by_day.n_orders is bigint")
check(schema.get("revenue") == "double", "orders_by_day.revenue is double")

# 2b. Capstone: the refunds contract.
refunds_schema = spark.table(f"{gold}.refunds_by_reason").schema
refunds = {f.name: f.dataType.simpleString() for f in refunds_schema}
check(refunds.get("reason") == "string", f"refunds_by_reason.reason is string ({refunds})")
check(refunds.get("n_refunds") == "bigint", "refunds_by_reason.n_refunds is bigint")
check(refunds.get("refunded") == "double", "refunds_by_reason.refunded is double")

# 3. Data arrived and is plausible.
stats = spark.sql(f"SELECT count(*) AS days, min(revenue) AS low FROM {gold}.orders_by_day").first()
check(stats.days > 0, f"orders_by_day has rows ({stats.days} days)")
check(stats.low is not None and stats.low > 0, "every day has positive revenue")

# COMMAND ----------

assert not failures, f"{len(failures)} integration check(s) failed: {failures}"
print("All integration checks passed.")
