# Lakeshore Outfitters — Databricks CI/CD course code

**Databricks CI/CD in Practice: Declarative Automation Bundles & GitHub Actions**<br>
by Fernando De Nitto

This repository is the reference project of the course: a Databricks platform shipped as a
**Declarative Automation Bundle** (formerly Databricks Asset Bundle) and released by a
**GitHub Actions** pipeline — pull-request checks, continuous deployment to staging,
approval-gated production, ephemeral PR environments, nightly drift detection.

It was built the way the course teaches it: **one pull request per lesson, every pull
request green before merge.** Each hands-on lesson's end state is a git tag; every production
release is a `v*` tag that went through the pipeline below.

## How to use it while you follow the course

Build your own repository lesson by lesson — that is the point. Use this one as the answer key:

```bash
git clone https://github.com/fernandodenitto/dbx-dab-cicd-prep-course-student.git
cd dbx-dab-cicd-prep-course-student
git tag -l 's*'                # one tag per hands-on lesson
git checkout s05-l03           # the project exactly as it is at the end of lesson 5.3
git diff s05-l02 s05-l03       # what one lesson changed
```

| Tags | Section |
|---|---|
| `s01-l03` | 1 · Toolbox |
| `s02-l02`, `s02-l04` | 2 · Bundles from zero |
| `s03-l01` … `s03-l03` | 3 · Git & the first CI |
| `s04-l02`, `s04-l03` | 4 · Service principals & CI authentication |
| `s05-l01` … `s05-l05` | 5 · One bundle, three environments |
| `s06-l01` … `s06-l03` | 6 · Code, artifacts & unit tests |
| `s07-l01` … `s07-l04` | 7 · Pipelines & jobs as code |
| `s08-l01`, `s08-l02` | 8 · Dashboards & drift |
| `s09-l02` … `s09-l06` | 9 · The release train |
| `s10-l01` … `s10-l04` | 10 · Advanced patterns for teams |
| `capstone` | Capstone: refunds analytics (release `v0.4.0`) |

## What's inside

```
databricks.yml              bundle: pinned CLI, variables, presets, permissions, targets dev/pr/staging/prod
resources/                  jobs, the orders pipeline, schemas + volume, the dashboard
src/lakeshore/              Python package (data generator + ingest entry point), built as a wheel
src/pipeline/               Lakeflow Spark Declarative Pipelines SQL (bronze → silver → gold)
src/notebooks/              health check, quality gate, integration test, weekly report
tests/                      pytest: package, release tooling, policy mutator
mutators.py                 company policy as code (owner tag required, default timeouts)
scripts/                    plan_report.py (PR plan, release gate, drift), check_dashboards.py, with_retry.sh
templates/data-product/     `databricks bundle init` template for new data products
bootstrap/                  one-time admin SQL: catalogs per environment, least-privilege grants
.github/workflows/          ci, cd-staging, cd-prod, pr-env, drift
.github/actions/setup/      the pinned toolchain (uv + Databricks CLI)
.github/setup/              GitHub environments as code
.github/rulesets/           branch protection as code
```

## Run it in your own accounts

You need: a **Databricks Free Edition** workspace, a **public** GitHub repository (GitHub Free
enforces environment reviewers and rulesets only on public repositories), the **Databricks CLI
≥ 1.19.0**, **uv** and the **GitHub CLI**.

1. `databricks auth login --host https://<your-workspace> --profile lakeshore` and
   `export DATABRICKS_CONFIG_PROFILE=lakeshore`; `uv sync`; `databricks bundle deploy` — your dev copy.
2. As a workspace admin: run `bootstrap/01_catalogs.sql`; create service principals
   `sp-lakeshore-staging` and `sp-lakeshore-prod` with OAuth secrets
   (Settings → Identity and access); run `bootstrap/02_grants.sql` with their application IDs.
3. `bash .github/setup/environments.sh <you>/<repo>`, then set `DATABRICKS_HOST`,
   `DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET` in environments `staging` (staging SP),
   `prod-plan` and `prod` (prod SP) with `gh secret set … --env <name>`.
4. Import `.github/rulesets/protect-main.json` (Settings → Rules → Rulesets → Import).
5. Open a pull request. Merge it. Tag `v0.1.0`. Approve the production deployment.

Free Edition is for learning and personal use, not for commercial workloads. Section 11 of the
course shows exactly which lines change on a paid, multi-workspace account.

## Never commit

Workspace URLs, client IDs, secrets, tokens, e-mail addresses. Hosts and credentials live in
GitHub environment secrets; everything else comes from bundle variables and lookups.
