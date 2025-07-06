import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your dataset
uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])
df['date'] = df['payment_timestamp'].dt.date
df = df.dropna(subset=["payer_id", "beneficiary_id", "payment_amount", "payment_alerted", "is_fraud"])

# Encode IDs
le_payer = LabelEncoder()
le_beneficiary = LabelEncoder()
df["payer_id_enc"] = le_payer.fit_transform(df["payer_id"])
df["beneficiary_id_enc"] = le_beneficiary.fit_transform(df["beneficiary_id"])

# Features and label
X = df[["payment_amount",  "payer_id_enc", "beneficiary_id_enc", "payment_alerted"]]
y = df["is_fraud"]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and encoders
joblib.dump(model, "fraud_model.pkl")
joblib.dump(le_payer, "payer_encoder.pkl")
joblib.dump(le_beneficiary, "beneficiary_encoder.pkl")
