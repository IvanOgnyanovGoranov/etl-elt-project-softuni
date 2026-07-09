from pandera import DataFrameSchema, Column, Check

sales_schema = DataFrameSchema( 
    { 
     "sales id": Column(int, checks=Check.ge(-1), nullable=False, ), 
     "proDuct id": Column(int, checks=Check.ge(-1), nullable=False, ), 
     "Region": Column(nullable=True), 
     "qty": Column(int, checks=Check.ge(0), nullable=False, ), 
     "Price": Column(float, checks=Check.ge(0), nullable=False)
     "Time stamp": Column( pa.DateTime, nullable=False, ), 
     "discount": Column(float, checks=Check.ge(0), nullable=False, ), 
     "order_status": Column(),
     }, 
     strict=True, # reject extra columns not defined here 
)

product_schema = DataFrameSchema( 
    { 
     "priduct_id": Column(int, checks=Check.ge(-1), nullable=False, ), 
     "category": Column(str, nullable=False, ), 
     "brand": Column(str, nullable=True), 
     "rating": Column(float, checks=Check.ge(0), nullable=False, ), 
     "in_stock": Column(bool, nullable=False),
     "launch_date": Column( pa.Date, nullable=False, ), 
     }, 
     strict=True, # reject extra columns not defined here 
)
    
