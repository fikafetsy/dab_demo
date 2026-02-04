import dlt
from pyspark.sql import functions as F

@dlt.table(
    name="silver_addresses_clean",
    comment="Cleaned addresses data",
    table_properties={"quality": "silver"},
)
@dlt.expect_or_fail("valid_customer_id", "customer_id IS NOT NULL")
@dlt.expect_or_drop("valid_address", "address_line_1 IS NOT NULL")
@dlt.expect("valid_postcode", "LENGTH(postcode) = 5")
def create_silver_addresses_clean():
    # Configuration from pipeline.yml -> configuration:
    source_catalog = spark.conf.get("source_catalog", "addresses_dev")
    bronze_schema = spark.conf.get("bronze_schema", "bronze")
    source_table = f"{source_catalog}.{bronze_schema}.bronze_addresses"
    
    return (
        spark.readStream.table(source_table)
        .select(
            "customer_id",
            "address_line_1",
            "city",
            "state",
            "postcode",
            F.col("created_date").cast("date").alias("created_date"),
        )
    )

dlt.create_streaming_table(
    name="silver_addresses",
    comment="SCD Type 2 addresses data",
    table_properties={"quality": "silver"},
)

# Apply CDC changes from the clean table in the same pipeline
dlt.create_auto_cdc_flow(
    target="silver_addresses",
    source="silver_addresses_clean",
    keys=["customer_id"],
    sequence_by="created_date",
    stored_as_scd_type=2,
)
