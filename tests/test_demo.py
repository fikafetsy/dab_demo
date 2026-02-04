def test_example(spark):
    """A simple test to verify the Spark session is working."""
    spark.sql("SELECT 1").show()
