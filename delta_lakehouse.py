import shutil
import pandas as pd
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable

def get_spark():
    builder = (
        SparkSession.builder
        .appName("customer-support-lakehouse")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

def run_lakehouse(input_path: str = "data/silver/validated_tweets.csv"):
    spark = get_spark()
    df = pd.read_csv(input_path)
    spark_df = spark.createDataFrame(df)

    bronze_path = "data/bronze/tweets"
    silver_path = "data/silver/tweets"
    gold_path = "data/gold/author_counts"

    for path in [bronze_path, silver_path, gold_path]:
        shutil.rmtree(path, ignore_errors=True)

    spark_df.write.format("delta").mode("overwrite").save(bronze_path)
    spark_df.limit(0).write.format("delta").mode("overwrite").save(silver_path)

    silver = DeltaTable.forPath(spark, silver_path)
    silver.alias("target").merge(
        spark_df.alias("source"),
        "target.tweet_id = source.tweet_id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

    gold = (
        spark.read.format("delta").load(silver_path)
        .groupBy("author_id")
        .count()
    )

    gold.write.format("delta").mode("overwrite").save(gold_path)
    print("Delta Lakehouse completed.")

if __name__ == "__main__":
    run_lakehouse()