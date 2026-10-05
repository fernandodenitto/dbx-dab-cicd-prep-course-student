-- SQL half of the health check. :catalog is the job parameter of the same name.
USE CATALOG IDENTIFIER(:catalog);

SELECT
  current_catalog() AS catalog,
  current_user()    AS run_as,
  count(*)          AS schemas_visible
FROM information_schema.schemata;
