import pandera as pa
from pandera import DataFrameSchema, Column, Check

output_sales_schema = DataFrameSchema(
    {
        "sales_id": Column(int, checks=Check.gt(0), nullable=False),
        "product_id": Column(int, checks=Check.gt(0), nullable=False),
        "region": Column(str, nullable=True),
        "qty": Column(int, checks=Check.ge(0), nullable=False),
        "price": Column(float, checks=Check.ge(0), nullable=False),
        "time_stamp": Column(pa.DateTime, nullable=False),
        "discount": Column(float, checks=Check.in_range(0, 1), nullable=False),
        "order_status": Column(str, nullable=True),
    },
    strict=True,
)

output_product_schema = DataFrameSchema(
    {
        "product_id": Column(int, checks=Check.gt(0), nullable=False),
        "category": Column(str, nullable=False),
        "brand": Column(str, nullable=True),
        "rating": Column(float, checks=Check.in_range(0, 5), nullable=False),
        "in_stock": Column(bool, nullable=False),
        "launch_date": Column(pa.DateTime, nullable=False),
    },
    strict=True,
)