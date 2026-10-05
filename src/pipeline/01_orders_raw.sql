-- BRONZE: every order file that lands in the volume, ingested incrementally.
-- ${landing_path} and ${bronze_schema} come from the pipeline's configuration, which
-- the bundle fills per target: no catalog, schema or path is written in this file.

CREATE OR REFRESH STREAMING TABLE ${bronze_schema}.orders_raw
COMMENT 'Raw orders, ingested incrementally from the landing volume'
AS SELECT
  *,
  _metadata.file_path AS source_file
FROM STREAM read_files(
  '${landing_path}/orders',
  format => 'json'
);
