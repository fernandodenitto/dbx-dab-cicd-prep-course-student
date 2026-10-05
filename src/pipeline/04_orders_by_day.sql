-- GOLD: daily revenue, recomputed by the pipeline as a materialized view.

CREATE OR REFRESH MATERIALIZED VIEW ${gold_schema}.orders_by_day
COMMENT 'Daily order count and revenue'
AS SELECT
  date(order_ts)            AS order_date,
  count(DISTINCT order_id)  AS n_orders,
  round(sum(line_total), 2) AS revenue
FROM order_items
GROUP BY date(order_ts);
