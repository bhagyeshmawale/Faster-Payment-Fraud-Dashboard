import streamlit as st
import pandas as pd

uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])

st.header("👤 Top Risky Users")

top_beneficiaries = df[df['is_fraud'] == 1].groupby('beneficiary_id').size().sort_values(ascending=False).head(10).reset_index(name='Fraud Count')
st.subheader("Top Beneficiaries Receiving Fraud")
st.bar_chart(top_beneficiaries,x='beneficiary_id',y='Fraud Count')

top_payers = df[df['is_fraud'] == 1].groupby('payer_id').size().sort_values(ascending=False).head(10).reset_index(name='Fraud Count')
print(top_payers.head())
st.subheader("Top Payers Sending Fraud")
st.bar_chart(top_payers,x='payer_id',y='Fraud Count')
