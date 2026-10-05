"""Company policy for every job in this bundle, enforced in code at deploy time.

Mutators run on every job — written in YAML or in Python — after variables and presets
are applied, before anything is deployed. Fix what is safe to fix; stop the deploy for
what isn't.
"""

from dataclasses import replace

from databricks.bundles.core import Bundle, job_mutator
from databricks.bundles.jobs import Job

DEFAULT_TIMEOUT_SECONDS = 4 * 3600


@job_mutator
def enforce_job_policy(bundle: Bundle, job: Job) -> Job:
    """Every job has an owner; no job can run forever."""
    # Not safe to guess: who is paged when this job fails? Stop the deploy.
    if not (job.tags or {}).get("owner"):
        raise ValueError(
            f"Job {job.name!r} has no 'owner' tag. Every job needs one "
            "(add `tags: ${var.tags}` to its definition)."
        )
    # Safe to fix: a job without a timeout gets the company default.
    if not job.timeout_seconds:
        job = replace(job, timeout_seconds=DEFAULT_TIMEOUT_SECONDS)
    return job
