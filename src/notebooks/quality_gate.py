# Databricks notebook source
# MAGIC %md
# MAGIC # Quality gate
# MAGIC
# MAGIC Runs after the pipeline. Every check is an `assert`: one failure fails the task, and
# MAGIC the job run turns red instead of quietly publishing bad numbers.

# COMMAND ----------

dbutils.widgets.text("catalog", "lakeshore_dev")
dbutils.widgets.text("silver_schema", "silver")
dbutils.widgets.text("gold_schema", "gold")
catalog = dbutils.widgets.get("catalog")
silver = f"{catalog}.{dbutils.widgets.get('silver_schema')}"
gold = f"{catalog}.{dbutils.widgets.get('gold_schema')}"

# COMMAND ----------

orders = spark.table(f"{silver}.orders")
n_orders = orders.count()
assert n_orders > 0, f"{silver}.orders is empty"

null_keys = orders.filter("order_id IS NULL OR customer_id IS NULL").count()
assert null_keys == 0, f"{null_keys} orders without keys passed the expectations"

# Gold must reconcile with silver to the cent: same revenue, computed two ways.
silver_revenue = (
    spark.sql(f"""
    SELECT round(sum(i.quantity * i.unit_price), 2) AS revenue
    FROM {silver}.orders LATERAL VIEW explode(items) AS i
""")
    .first()
    .revenue
)
gold_revenue = (
    spark.sql(f"SELECT round(sum(revenue), 2) AS revenue FROM {gold}.orders_by_day").first().revenue
)
assert silver_revenue == gold_revenue, f"gold {gold_revenue} != silver {silver_revenue}"

print(f"OK: {n_orders} orders, revenue {gold_revenue} reconciles silver -> gold")
