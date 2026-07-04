import pandas as pd
import great_expectations as gx

def run_validation(input_path: str = "data/silver/validated_tweets.csv"):
    df = pd.read_csv(input_path)
    validator = gx.from_pandas(df)

    validator.expect_column_values_to_not_be_null("tweet_id")
    validator.expect_column_values_to_not_be_null("author_id")
    validator.expect_column_values_to_not_be_null("text")
    validator.expect_column_values_to_be_unique("tweet_id")
    validator.expect_column_value_lengths_to_be_between("text", min_value=5, max_value=5000)
    validator.expect_column_values_to_not_be_null("created_at")

    results = validator.validate()
    print("Great Expectations success:", results["success"])
    return results

if __name__ == "__main__":
    run_validation()