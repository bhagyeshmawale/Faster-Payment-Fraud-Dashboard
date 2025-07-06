import streamlit as st
import pandas as pd

uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])

st.header("📊 Overview Metrics")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Transactions", len(df))
col2.metric("Total Value Sent", f"£{df['payment_amount'].sum():,.2f}")
col3.metric("Frauds", df["is_fraud"].sum())
col4.metric("Alerts Raised", df["payment_alerted"].sum())

st.markdown(f"Total Fraud Transaction Value £{df[df['is_fraud']==1]['payment_amount'].sum():,.2f}")
st.markdown(f"Total Fraud Alerted Value £{df[df['payment_alerted']==1]['payment_amount'].sum():,.2f}")

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.dataframe(df[['event_id', 'payer_id', 'beneficiary_id', 'payment_timestamp', 'payment_amount','is_fraud','payment_alerted']])


