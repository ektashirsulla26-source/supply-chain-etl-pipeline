# model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

df = pd.read_csv('data/clean_data.csv')

FEATURES = ['Days for shipment (scheduled)', 'shipping_enc',
            'Sales', 'Order Item Quantity',
            'order_month', 'delay_days']
TARGET = 'Late_delivery_risk'

X = df[FEATURES].fillna(0)
y = df[TARGET]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train model
print("Training model... please wait")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Print accuracy
print(classification_report(y_test, model.predict(X_test)))

# Save model
pickle.dump(model, open('model.pkl', 'wb'))
print("✓ Model saved!")

# Save predictions
df['predicted_late'] = model.predict(X.fillna(0))
df['confidence_score'] = model.predict_proba(X.fillna(0))[:,1].round(2)
df[['Order Id','predicted_late','confidence_score']].to_csv(
    'data/predictions.csv', index=False)
print("✓ Predictions saved to data/predictions.csv")
