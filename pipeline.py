# pipeline.py — run this file to execute the full project
from extract import extract
from transform import transform
from load import load
import subprocess

print("--- Step 1: Extract ---")
df = extract()

print("--- Step 2: Transform ---")
df = transform(df)

print("--- Step 3: Load to PostgreSQL ---")
load(df)

print("--- Step 4: Train ML Model ---")
subprocess.run(['python', 'model.py'], check=True)

print("\n✓ Full pipeline complete! Check pgAdmin + data/predictions.csv")