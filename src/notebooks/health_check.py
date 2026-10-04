# Databricks notebook source
# MAGIC %md
# MAGIC # Lakeshore health check
# MAGIC
# MAGIC Deployed by the bundle. If this notebook runs, three things are true: the files
# MAGIC were synced, the job definition was created, and serverless compute works.

# COMMAND ----------

dbutils.widgets.text("target", "dev")
target = dbutils.widgets.get("target")

row = spark.sql("SELECT current_user() AS who, current_catalog() AS catalog").first()
print(f"target  : {target}")
print(f"user    : {row.who}")
print(f"catalog : {row.catalog}")
print(f"spark   : {spark.version}")

# COMMAND ----------

dbutils.notebook.exit(f"healthy:{target}")
