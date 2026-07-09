

def validate_sales_data(df: pd.DataFrame) -> pd.DataFrame: 
    validated_df = sales_schema.validate(df) 
    return validated_df

def validate_product_data(df: pd.DataFrame) -> pd.DataFrame: 
    validated_df = sales_schema.validate(df) 
    return validated_df