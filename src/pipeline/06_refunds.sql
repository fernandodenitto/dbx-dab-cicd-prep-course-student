-- CAPSTONE · SILVER: the packed "REASON|source" column split in two; refunds must be positive.

CREATE OR REFRESH STREAMING TABLE ${silver_schema}.refunds (
  CONSTRAINT positive_amount EXPECT (amount > 0) ON VIOLATION DROP ROW,
  CONSTRAINT known_reason    EXPECT (reason IS NOT NULL)
)
COMMENT 'Refunds with reason and source as separate columns'
AS SELECT
  refund_id,
  payment_id,
  refund_ts,
  amount,
  split_part(reason, '|', 1) AS reason,
  split_part(reason, '|', 2) AS source
FROM STREAM(${bronze_schema}.refunds_raw);
