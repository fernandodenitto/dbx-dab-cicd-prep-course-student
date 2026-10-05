-- One row per order line. A temporary view: private to the pipeline, never published.

CREATE TEMPORARY VIEW order_items AS
SELECT
  order_id,
  order_ts,
  item.product_id,
  item.quantity,
  item.unit_price,
  item.quantity * item.unit_price AS line_total
FROM (
  SELECT order_id, order_ts, explode(items) AS item
  FROM ${silver_schema}.orders
);
