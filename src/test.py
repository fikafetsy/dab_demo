try:
    from databricks.connect import DatabricksSession

    spark = DatabricksSession.builder.getOrCreate()
    print("==> Using DatabricksSession.")
except Exception as e:
    # databricks.connect may raise non-ImportError exceptions on incompatible environments;
    # fall back to local pyspark when any error occurs during import/initialization.
    try:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        print("==> Using Local SparkSession.")
    except ImportError:
        raise ImportError("Neither DatabricksSession nor SparkSession could be imported.") from e