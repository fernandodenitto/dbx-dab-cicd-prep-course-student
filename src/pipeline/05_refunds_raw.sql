-- CAPSTONE · BRONZE: refund files from the landing volume, ingested incrementally.

CREATE OR REFRESH STREAMING TABLE ${bronze_schema}.refunds_raw
COMMENT 'Raw refunds, ingested incrementally from the landing volume'
AS SELECT
  *,
  _metadata.file_path AS source_file
FROM STREAM read_files(
  '${landing_path}/refunds',
  format => 'csv',
  header => true
);
