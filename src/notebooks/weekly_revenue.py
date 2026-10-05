# Databricks notebook source
# MAGIC %md
# MAGIC # Weekly revenue report
# MAGIC
# MAGIC Originally built by hand in the UI; now deployed by the bundle. The catalog and
# MAGIC schema arrive as parameters instead of being written into the query.

# COMMAND ----------

dbutils.widgets.text("catalog", "lakeshore_dev")
dbutils.widgets.text("gold_schema", "gold")
table = f"{dbutils.widgets.get('catalog')}.{dbutils.widgets.get('gold_schema')}.orders_by_day"

df = spark.sql(f"""
  SELECT round(sum(revenue), 2) AS revenue_last_7_days
  FROM {table}
  WHERE order_date >= date_sub((SELECT max(order_date) FROM {table}), 7)
""")
display(df)
