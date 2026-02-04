def get_spark_session():
    try:
        from databricks.connect import DatabricksSession

        spark = DatabricksSession.builder.getOrCreate()
        print("==> Using DatabricksSession.")
        return spark

    except Exception as e:
        # 2) Fallback to local PySpark
        try:
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.getOrCreate()
            print("==> Using Local SparkSession.")
            return spark
        except Exception:
            raise ImportError(
                "Failed to initialize Databricks Connect AND local PySpark. "
                "Likely dependency mismatch (pyspark vs databricks-connect)."
            ) from e


get_spark_session()
