import logging
import pandas as pd
from pandera.errors import SchemaErrors

from include.validations.output_schemas import output_sales_schema, output_product_schema

logging.basicConfig(
    filename="logs/validation.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_output_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        validated_df = output_sales_schema.validate(df, lazy=True)
        return validated_df
    except SchemaErrors as err:
        logging.warning(f"Output sales validation failures:\n{err.failure_cases}")
        bad_indices = err.failure_cases["index"].dropna().unique()
        clean_df = df.drop(index=bad_indices, errors="ignore")
        logging.warning(f"Dropped {len(bad_indices)} invalid transformed sales rows.")
        return clean_df


def validate_output_product_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        validated_df = output_product_schema.validate(df, lazy=True)
        return validated_df
    except SchemaErrors as err:
        logging.warning(f"Output product validation failures:\n{err.failure_cases}")
        bad_indices = err.failure_cases["index"].dropna().unique()
        clean_df = df.drop(index=bad_indices, errors="ignore")
        logging.warning(f"Dropped {len(bad_indices)} invalid transformed product rows.")
        return clean_df


if __name__ == "__main__":
    from include.etl.extract_s3 import sales_data_df, product_data_df
    from include.validations.validate_inputs import validate_sales_data, validate_product_data
    from include.etl.transform import transform_sales_data, transform_product_data

    clean_sales = validate_sales_data(sales_data_df)
    clean_products = validate_product_data(product_data_df)

    transformed_sales = transform_sales_data(clean_sales)
    transformed_products = transform_product_data(clean_products)

    final_sales = validate_output_sales_data(transformed_sales)
    final_products = validate_output_product_data(transformed_products)

    print(f"Sales: {len(transformed_sales)} rows in, {len(final_sales)} rows valid")
    print(f"Products: {len(transformed_products)} rows in, {len(final_products)} rows valid")