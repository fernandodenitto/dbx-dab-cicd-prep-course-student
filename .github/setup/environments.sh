#!/usr/bin/env bash
# GitHub environments for this repository, as code. Run once with the GitHub CLI:
#   bash .github/setup/environments.sh <owner>/<repo>
# Then set DATABRICKS_HOST / DATABRICKS_CLIENT_ID / DATABRICKS_CLIENT_SECRET in each
# environment with `gh secret set <NAME> --repo <owner>/<repo> --env <environment>`:
#   staging            -> staging service principal
#   prod-plan, prod    -> production service principal
set -euo pipefail
REPO="$1"
ME=$(gh api user -q .id)

gh api -X PUT "repos/$REPO/environments/staging" >/dev/null

# prod-plan: shows the production plan before approval; only main and release tags.
gh api -X PUT "repos/$REPO/environments/prod-plan" --input - >/dev/null <<JSON
{"deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}
JSON

# prod: a required reviewer (you; in a team, the release owners), same branch rules.
gh api -X PUT "repos/$REPO/environments/prod" --input - >/dev/null <<JSON
{"reviewers": [{"type": "User", "id": $ME}], "prevent_self_review": false,
 "deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}
JSON

for env in prod-plan prod; do
  gh api -X POST "repos/$REPO/environments/$env/deployment-branch-policies" -f name='v*' -f type=tag >/dev/null
  gh api -X POST "repos/$REPO/environments/$env/deployment-branch-policies" -f name=main -f type=branch >/dev/null
done
echo "Environments staging, prod-plan, prod configured for $REPO."
