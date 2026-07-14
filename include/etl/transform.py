import logging
import pandas as pd

from include.validations.validate_inputs import validate_sales_data, validate_product_data
from include.etl.extract_s3 import sales_data_df, product_data_df

logging.basicConfig(
    filename="logs/validation.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df["time_stamp"] = pd.to_datetime(df["time_stamp"], format="mixed", errors="coerce")
    df["region"] = df["region"].str.strip().str.title()
    df["total_revenue"] = df["qty"] * df["price"] * (1 - df["discount"])

    logging.info(f"Transformed sales data: {len(df)} rows")
    return df


def transform_product_data(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    df["launch_date"] = pd.to_datetime(df["launch_date"], format="mixed", errors="coerce")

    logging.info(f"Transformed product data: {len(df)} rows")
    return df


if __name__ == "__main__":
    clean_sales = validate_sales_data(sales_data_df)
    clean_products = validate_product_data(product_data_df)

    transformed_sales = transform_sales_data(clean_sales)
    transformed_products = transform_product_data(clean_products)

    print(transformed_sales.head())
    print(transformed_products.head())