import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")

print("KEY:", AWS_KEY)
print("SECRET starts with:", AWS_SECRET[:4] if AWS_SECRET else None)

product_df = pd.read_csv("s3://data-warehouse-course-l1/course-project/sales_data.csv", storage_options={"key": AWS_KEY, "secret": AWS_SECRET})

print(product_df.head())
