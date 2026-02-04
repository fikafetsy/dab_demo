import dlt
from pyspark.sql import functions as F

@dlt.table(
    name="bronze_addresses",
    table_properties={"quality": "bronze"},
    comment="Raw addresses data ingested from the source system"
)
def create_bronze_addresses():
    source_catalog = spark.conf.get("source_catalog", "addresses_dev")
    landing_schema = spark.conf.get("landing_schema", "landing")
    source_folder = spark.conf.get("source_folder", "source_addresses")
    source_path = f"/Volumes/{source_catalog}/{landing_schema}/{source_folder}/"
    
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.inferColumnTypes", "true")
            .load(source_path)
            .select(
                "*",
                F.col("_metadata.file_path").alias("input_file_path"),
                F.current_timestamp().alias("ingest_timestamp")
            )
    )