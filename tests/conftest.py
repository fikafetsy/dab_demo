"""Pytest configuration and fixtures for Spark.

This module avoids importing `databricks.connect` at module import time
because that package may raise non-ImportError exceptions in environments
without a compatible SparkSession. Imports of Databricks-specific APIs are
performed lazily inside fixtures or helper functions and guarded with
broad exception handlers to allow falling back to a local `pyspark` session.
"""

import csv
import json
import os
import pathlib
import sys
from contextlib import contextmanager

import pytest


@pytest.fixture()
def spark():
    """Return a SparkSession — prefer Databricks Connect when available.

    This tries to import and initialize `DatabricksSession`. Any exception
    during that process is caught and we fall back to a local
    `pyspark.sql.SparkSession`.
    """
    try:
        from databricks.connect import DatabricksSession

        spark = DatabricksSession.builder.getOrCreate()
        print("==> Using DatabricksSession.")
        return spark
    except Exception:
        try:
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.getOrCreate()
            print("==> Using Local SparkSession.")
            return spark
        except ImportError:
            raise ImportError("Neither DatabricksSession nor SparkSession could be imported.")


@pytest.fixture()
def load_fixture(spark):
    """Callable fixture to load JSON or CSV files from the `fixtures/` directory."""

    def _loader(filename: str):
        path = pathlib.Path(__file__).parent.parent / "fixtures" / filename
        suffix = path.suffix.lower()
        if suffix == ".json":
            rows = json.loads(path.read_text())
            return spark.createDataFrame(rows)
        if suffix == ".csv":
            with path.open(newline="") as f:
                rows = list(csv.DictReader(f))
            return spark.createDataFrame(rows)
        raise ValueError(f"Unsupported fixture type for: {filename}")

    return _loader


def _enable_fallback_compute():
    """Enable serverless compute if no compute is specified.

    This uses `databricks.sdk.WorkspaceClient` if available; failure to import
    or initialize the client is ignored because it's only an advisory helper
    for tests running against Databricks.
    """
    try:
        from databricks.sdk import WorkspaceClient

        conf = WorkspaceClient().config
        if conf.serverless_compute_id or conf.cluster_id or os.environ.get("SPARK_REMOTE"):
            return

        url = "https://docs.databricks.com/dev-tools/databricks-connect/cluster-config"
        print("☁️ no compute specified, falling back to serverless compute", file=sys.stderr)
        print(f"  see {url} for manual configuration", file=sys.stdout)

        os.environ["DATABRICKS_SERVERLESS_COMPUTE_ID"] = "auto"
    except Exception:
        # If the SDK isn't present or fails to initialize, skip fallback.
        return


@contextmanager
def _allow_stderr_output(config: pytest.Config):
    """Temporarily disable pytest output capture."""
    capman = config.pluginmanager.get_plugin("capturemanager")
    if capman:
        with capman.global_and_fixture_disabled():
            yield
    else:
        yield


def pytest_configure(config: pytest.Config):
    """Configure pytest session and attempt to prepare Databricks compute.

    Initialization of Databricks-specific builders is attempted lazily and
    guarded so that tests can still run locally when Databricks packages are
    present but not fully functional in the environment.
    """
    with _allow_stderr_output(config):
        _enable_fallback_compute()

        try:
            # Validate or create a remote session only if Databricks Connect is
            # available and behaves as expected. Any exception here should not
            # prevent tests from running with the local Spark fallback.
            from databricks.connect import DatabricksSession

            if hasattr(DatabricksSession.builder, "validateSession"):
                DatabricksSession.builder.validateSession().getOrCreate()
            else:
                DatabricksSession.builder.getOrCreate()
        except Exception:
            # Ignore errors during eager Databricks initialization.
            return
