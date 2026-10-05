# Databricks notebook source
# MAGIC %md
# MAGIC # Lakeshore health check
# MAGIC
# MAGIC Deployed by the bundle. If this notebook runs, three things are true: the files
# MAGIC were synced, the job definition was created, and serverless compute works.

# COMMAND ----------

dbutils.widgets.text("target", "dev")
dbutils.widgets.text("catalog", "lakeshore_dev")
target = dbutils.widgets.get("target")
catalog = dbutils.widgets.get("catalog")

# Fails if the environment's catalog is missing or this identity can't use it.
spark.sql(f"USE CATALOG {catalog}")
row = spark.sql("SELECT current_user() AS who, current_catalog() AS catalog").first()
print(f"target  : {target}")
print(f"user    : {row.who}")
print(f"catalog : {row.catalog}")
print(f"spark   : {spark.version}")

# COMMAND ----------

dbutils.notebook.exit(f"healthy:{target}")
