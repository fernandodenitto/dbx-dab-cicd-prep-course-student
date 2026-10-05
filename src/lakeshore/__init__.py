"""Lakeshore Outfitters data platform — the Python code the bundle deploys."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lakeshore")
except PackageNotFoundError:  # running from a source checkout without installing
    __version__ = "0.0.0+local"
