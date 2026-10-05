"""The job policy, tested without a workspace: mutators are plain Python functions."""

import pytest
from databricks.bundles.core import Bundle
from databricks.bundles.jobs import Job

from mutators import DEFAULT_TIMEOUT_SECONDS, enforce_job_policy

BUNDLE = Bundle(target="dev")
policy = enforce_job_policy.function


def test_job_without_owner_stops_the_deploy():
    with pytest.raises(ValueError, match="no 'owner' tag"):
        policy(BUNDLE, Job(name="orphan", tags={"project": "x"}))


def test_missing_timeout_gets_the_default():
    job = policy(BUNDLE, Job(name="ok", tags={"owner": "data-platform"}))
    assert job.timeout_seconds == DEFAULT_TIMEOUT_SECONDS


def test_explicit_timeout_is_kept():
    job = policy(BUNDLE, Job(name="ok", tags={"owner": "a"}, timeout_seconds=3600))
    assert job.timeout_seconds == 3600
