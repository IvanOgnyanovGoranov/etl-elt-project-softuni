import io
import logging
import pandas as pd

from include.etl.extract_s3 import S3, config

logging.basicConfig(
    filename="logs/validation.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_parquet_to_s3(df: pd.DataFrame, bucket: str, full_path: str) -> None:
    """Write a DataFrame to S3 as Parquet, entirely in-memory (no local temp file)."""
    buffer = io.BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)  # rewind before reading, since to_parquet leaves the cursor at the end

    S3.put_object(Bucket=bucket, Key=full_path, Body=buffer.getvalue())

    logging.info(f"Uploaded {len(df)} rows to s3://{bucket}/{full_path}")
    print(f"Saved {len(df)} rows to s3://{bucket}/{full_path}")


if __name__ == "__main__":
    from include.etl.extract_s3 import sales_data_df, product_data_df
    from include.validations.validate_inputs import validate_sales_data, validate_product_data
    from include.etl.transform import transform_sales_data, transform_product_data
    from include.validations.validate_outputs import validate_output_sales_data, validate_output_product_data

    clean_sales = validate_sales_data(sales_data_df)
    clean_products = validate_product_data(product_data_df)

    transformed_sales = transform_sales_data(clean_sales)
    transformed_products = transform_product_data(clean_products)

    final_sales = validate_output_sales_data(transformed_sales)
    final_products = validate_output_product_data(transformed_products)

    bucket = config["s3"]["bucket"]
    processed_prefix = config["s3"]["processed_prefix"]

    load_parquet_to_s3(final_sales, bucket, f"{processed_prefix}sales_data.parquet")
    load_parquet_to_s3(final_products, bucket, f"{processed_prefix}product_data.parquet")