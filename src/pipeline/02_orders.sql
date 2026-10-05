-- SILVER: typed, validated orders. Expectations drop rows that can't be trusted and
-- record a warning for the ones that merely look odd.

CREATE OR REFRESH STREAMING TABLE ${silver_schema}.orders (
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL)    ON VIOLATION DROP ROW,
  CONSTRAINT valid_customer EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT sane_timestamp EXPECT (order_ts <= current_timestamp())
)
COMMENT 'Cleaned orders with declared quality expectations'
AS SELECT
  order_id,
  customer_id,
  CAST(order_ts AS TIMESTAMP) AS order_ts,
  items,
  source_file
FROM STREAM(${bronze_schema}.orders_raw);
