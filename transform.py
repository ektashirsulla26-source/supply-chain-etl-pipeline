# transform.py
import pandas as pd
import numpy as np

def transform(df):
    # Remove columns we don't need
    df = df.drop(columns=['Customer Password','Product Image'], errors='ignore')

    # Fix date columns
    df['order_date'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')

    # Create new useful columns
    df['delay_days'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
    df['profit_margin'] = (df['Order Profit Per Order'] / df['Sales'].replace(0, np.nan)) * 100
    df['order_month']   = df['order_date'].dt.month
    df['order_year']    = df['order_date'].dt.year

    # Encode shipping mode as number for ML
    df['shipping_enc'] = df['Shipping Mode'].astype('category').cat.codes

    # Fill missing values
    df.fillna(0, inplace=True)

    print(f"✓ Transform done. Shape: {df.shape}")
    df.to_csv('data/clean_data.csv', index=False)
    return df

if __name__ == "__main__":
    from extract import extract
    df = extract()
    df = transform(df)