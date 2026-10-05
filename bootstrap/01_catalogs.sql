-- Bootstrap, step 1 — run ONCE, as a workspace admin (SQL editor, or the CLI).
--
-- One Free Edition workspace, three environments: each environment is a catalog.
-- Catalogs are created here, by a human admin, and NOT by the bundle: the identities
-- that deploy the bundle must never hold CREATE CATALOG.

CREATE CATALOG IF NOT EXISTS lakeshore_dev
  COMMENT 'Lakeshore platform: development (personal dev deploys and PR environments)';

CREATE CATALOG IF NOT EXISTS lakeshore_staging
  COMMENT 'Lakeshore platform: staging (deployed by CI on every merge to main)';

CREATE CATALOG IF NOT EXISTS lakeshore_prod
  COMMENT 'Lakeshore platform: production (deployed by CI after approval)';

-- In a team, developers get their own sandbox rights on the dev catalog only:
-- GRANT USE CATALOG, CREATE SCHEMA ON CATALOG lakeshore_dev TO `data-engineers`;
