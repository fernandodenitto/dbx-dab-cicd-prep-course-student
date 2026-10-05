-- CAPSTONE · GOLD: what customers send back, and why.

CREATE OR REFRESH MATERIALIZED VIEW ${gold_schema}.refunds_by_reason
COMMENT 'Refund count and amount per reason'
AS SELECT
  reason,
  count(*)              AS n_refunds,
  round(sum(amount), 2) AS refunded
FROM ${silver_schema}.refunds
GROUP BY reason;
