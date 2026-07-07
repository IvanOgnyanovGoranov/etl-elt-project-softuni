import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")

sales_data_df = pd.read_csv("s3://data-warehouse-course-l1/course-project/sales_data.csv", storage_options={"key": AWS_KEY, "secret": AWS_SECRET})
product_data_df = pd.read_json("s3://data-warehouse-course-l1/course-project/product_data.json", storage_options={"key": AWS_KEY, "secret": AWS_SECRET})

print(sales_data_df.head())
print(product_data_df.head())
