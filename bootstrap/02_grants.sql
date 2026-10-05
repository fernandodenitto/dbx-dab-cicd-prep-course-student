-- Bootstrap, step 2 — run ONCE, as a workspace admin, after creating the two service
-- principals (Settings → Identity and access → Service principals).
--
-- Replace the placeholders with each service principal's APPLICATION ID (a UUID).
-- In SQL a service principal is named by its application ID, in backticks.
--
-- Least privilege: each deployer can create schemas (and then owns them) in its own
-- catalog, and has no privilege at all anywhere else.

-- staging deployer: the staging catalog, plus the dev catalog for PR environments (S10)
GRANT USE CATALOG, CREATE SCHEMA ON CATALOG lakeshore_staging TO `<STAGING_SP_APPLICATION_ID>`;
GRANT USE CATALOG, CREATE SCHEMA ON CATALOG lakeshore_dev     TO `<STAGING_SP_APPLICATION_ID>`;

-- production deployer: the production catalog only
GRANT USE CATALOG, CREATE SCHEMA ON CATALOG lakeshore_prod    TO `<PROD_SP_APPLICATION_ID>`;
