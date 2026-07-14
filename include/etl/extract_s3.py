import os
import io
import yaml
import boto3
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")


with open("include/config.yaml", "r") as f:
    config = yaml.safe_load(f)


S3 = boto3.client(
    's3',
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET
)

# Add try except block for both functions
def extract_csv(bucket: str, full_path: str) -> pd.DataFrame:
    """Fetch a CSV object from S3 and load it into a DataFrame."""
    csv_object = S3.get_object(Bucket=bucket, Key=full_path)
    df = pd.read_csv(csv_object['Body'])
    return df

def extract_json(bucket: str, full_path: str) -> pd.DataFrame:
    """Fetch a JSON object from S3 and load it into a DataFrame."""
    json_object = S3.get_object(Bucket=bucket, Key=full_path)
    json_bytes = json_object['Body'].read()
    json_str = json_bytes.decode('utf-8')       
    df = pd.read_json(io.StringIO(json_str))
    return df


sales_data_df = extract_csv(
    config['s3']['bucket'],
    config['s3']['raw_prefix'] + config['s3']['sales_file']
)

product_data_df = extract_json(
    config['s3']['bucket'],
    config['s3']['raw_prefix'] + config['s3']['products_file']
)

if __name__ == "__main__":
    print(sales_data_df.info())
    print(product_data_df.info())