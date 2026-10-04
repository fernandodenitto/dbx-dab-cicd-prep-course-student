# Lakeshore Outfitters — Databricks CI/CD course code

**Databricks CI/CD in Practice: Declarative Automation Bundles & GitHub Actions**<br>
by Fernando De Nitto

This repository is the reference project of the course: a Databricks platform shipped as a
**Declarative Automation Bundle** (formerly Databricks Asset Bundle) and released by a
**GitHub Actions** pipeline — pull request checks, continuous deployment to staging,
approval-gated production.

It was built the way the course teaches it: **one pull request per lesson, every pull
request green before merge.** Each lesson's end state is a git tag.

## How to use it while you follow the course

Build your own repository lesson by lesson — that is the point. Use this one as the
answer key:

```bash
git clone https://github.com/fernandodenitto/dbx-dab-cicd-prep-course-student.git
cd dbx-dab-cicd-prep-course-student
git tag -l                     # one tag per hands-on lesson, e.g. s02-l02
git checkout s02-l02           # the project exactly as it is at the end of lesson 2.2
git diff s02-l02 s02-l03       # what one lesson changed
```

Fell behind? Copy the files from the tag of the lesson you are about to start.

## What you need

- A **Databricks Free Edition** workspace — free, no cloud account
  (<https://www.databricks.com/learn/free-edition>).
- A **GitHub** account (free plan). Your course repository must be **public**: on the free
  plan, environments with required reviewers and branch rulesets only work on public
  repositories.
- The **Databricks CLI ≥ 1.19.0**, **uv**, **git**, and optionally the **GitHub CLI** (`gh`).

Free Edition is for learning and personal use, not for commercial workloads. Everything
here maps one-to-one onto a paid workspace — the course shows exactly which lines change.

## Never commit

Workspace URLs, client IDs, secrets, tokens, e-mail addresses. Hosts and credentials live
in GitHub variables and secrets; everything else comes from bundle substitutions.
