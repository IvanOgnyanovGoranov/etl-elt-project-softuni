import pandera as pa
from pandera import DataFrameSchema, Column, Check

input_sales_schema = DataFrameSchema(
    {
        "sales id": Column(int, checks=Check.gt(0), nullable=False),
        "proDuct Id": Column(int, checks=Check.gt(0), nullable=False),
        "Region": Column(str, nullable=True),
        "qty": Column(int, checks=Check.ge(0), nullable=False),
        "Price": Column(float, checks=Check.ge(0), nullable=False),
        "Time stamp": Column(pa.DateTime, coerce=True, nullable=False),
        "discount": Column(float, checks=Check.ge(0), nullable=False),
        "order_status": Column(str, nullable=True),
    },
    strict=True,
)

input_product_schema = DataFrameSchema(
    {
        "product_id": Column(int, checks=Check.gt(0), nullable=False),
        "category": Column(str, nullable=False),
        "brand": Column(str, nullable=True),
        "rating": Column(float, checks=Check.ge(0), nullable=False),
        "in_stock": Column(bool, nullable=False),
        "launch_date": Column(pa.DateTime, coerce=True, nullable=False),
    },
    strict=True,
)