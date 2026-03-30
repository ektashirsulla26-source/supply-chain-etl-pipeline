# load.py
from sqlalchemy import create_engine, URL
import pandas as pd

DB = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Sumit@2803",
    host="localhost",
    port=5432,
    database="supply_chain_db"
)

def load(df):
    engine = create_engine(DB)

    customers = df[['Customer Id','Customer Fname',
                    'Customer Segment','Customer City']].drop_duplicates()
    customers.to_sql('dim_customers', engine, if_exists='replace', index=False)
    print("✓ dim_customers loaded!")

    orders = df[['Order Id','Customer Id','Shipping Mode',
                 'order_date','Sales','Order Profit Per Order',
                 'delay_days','Late_delivery_risk',
                 'order_month','order_year','profit_margin']].copy()
    orders.to_sql('fact_orders', engine, if_exists='replace', index=False)
    print("✓ fact_orders loaded!")
    print("✓ Data successfully loaded to PostgreSQL!")

if __name__ == "__main__":
    from extract import extract
    from transform import transform
    df = extract()
    df = transform(df)
    load(df)
