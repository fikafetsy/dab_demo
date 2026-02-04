from pyspark.sql import functions as F

def build_source_path(spark) -> str:
    source_catalog = spark.conf.get("source_catalog", "addresses_dev")
    landing_schema = spark.conf.get("landing_schema", "landing")
    source_folder = spark.conf.get("source_folder", "source_addresses")
    return f"/Volumes/{source_catalog}/{landing_schema}/{source_folder}/"

def bronze_addresses_df(spark):
    source_path = build_source_path(spark)
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(source_path)
        .select(
            "*",
            F.col("_metadata.file_path").alias("input_file_path"),
            F.current_timestamp().alias("ingest_timestamp"),
        )
    )
