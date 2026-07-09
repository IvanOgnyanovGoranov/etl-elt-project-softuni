import os
import logging
import pandas as pd
from pandera.errors import SchemaErrors
from include.validations.input_schemas import sales_schema, product_schema

# --- Logger setup ---
os.makedirs("logs", exist_ok=True)  # creates logs/ folder if it doesn't exist yet

logging.basicConfig(
    filename="logs/validation.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        validated_df = sales_schema.validate(df, lazy=True)
        return validated_df
    except SchemaErrors as err:
        logging.warning(f"Sales validation failures:\n{err.failure_cases}")
        bad_indices = err.failure_cases["index"].dropna().unique()
        clean_df = df.drop(index=bad_indices, errors="ignore")
        logging.warning(f"Dropped {len(bad_indices)} invalid sales rows.")
        return clean_df

def validate_product_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        validated_df = product_schema.validate(df, lazy=True)
        return validated_df
    except SchemaErrors as err:
        logging.warning(f"Product validation failures:\n{err.failure_cases}")
        bad_indices = err.failure_cases["index"].dropna().unique()
        clean_df = df.drop(index=bad_indices, errors="ignore")
        logging.warning(f"Dropped {len(bad_indices)} invalid product rows.")
        return clean_df
    

if __name__ == "__main__":
    from include.etl.extract_s3 import sales_data_df, product_data_df

    clean_sales = validate_sales_data(sales_data_df)
    clean_products = validate_product_data(product_data_df)

    print(f"Sales: {len(sales_data_df)} rows in, {len(clean_sales)} rows valid")
    print(f"Products: {len(product_data_df)} rows in, {len(clean_products)} rows valid")