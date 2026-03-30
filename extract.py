# extract.py
import pandas as pd

def extract():
    df = pd.read_csv('data/DataCoSupplyChainDataset.csv',
                     encoding='latin-1')
    print(f"✓ Loaded {len(df)} rows and {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    df = extract()
    print(df.head(2))