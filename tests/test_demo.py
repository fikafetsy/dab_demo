def test_example(spark):
    spark.sql("SELECT 1").show()