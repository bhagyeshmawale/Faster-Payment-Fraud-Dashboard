import streamlit as st
import pandas as pd
import joblib

st.title("🧠 Fraud Risk Predictor")

model = joblib.load("fraud_model.pkl")
payer_encoder = joblib.load("payer_encoder.pkl")
beneficiary_encoder = joblib.load("beneficiary_encoder.pkl")

# Input UI
# payer_age = st.slider("Payer Age", 18, 90, 30)
payment_amount = st.number_input("Payment Amount (£)", value=500.0)
payer_id = st.text_input("Payer ID (e.g., C001)")
beneficiary_id = st.text_input("Beneficiary ID (e.g., B001)")
payment_alerted = st.selectbox("Was this transaction alerted by rules?", [0, 1])

if st.button("Predict Fraud Risk"):
    payer_id_enc = payer_encoder.transform([payer_id])[0] if payer_id in payer_encoder.classes_ else 0
    beneficiary_id_enc = beneficiary_encoder.transform([beneficiary_id])[0] if beneficiary_id in beneficiary_encoder.classes_ else 0

    input_df = pd.DataFrame([{
        "payment_amount": payment_amount,
        # "payer_age": payer_age,
        "payer_id_enc": payer_id_enc,
        "beneficiary_id_enc": beneficiary_id_enc,
        "payment_alerted": payment_alerted
    }])

    proba = model.predict_proba(input_df)[0, 1]
    st.metric("📊 Predicted Fraud Probability", f"{proba:.2%}")

    if proba > 0.5:
        st.error("⚠️ High Fraud Risk")
    else:
        st.success("✅ Low Fraud Risk")
