import streamlit as st
import pandas as pd
import plotly.express as px


uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])
df['date'] = df['payment_timestamp'].dt.date

st.header("📅 Daily Fraud & Alert Trends")

daily = df.groupby("date").agg(
    frauds=('is_fraud', 'sum'),
    alerts=('payment_alerted', 'sum'),
    txns=('payment_amount', 'count')
).reset_index()

fig = px.line(daily, x='date', y=['frauds', 'alerts'], title='Frauds and Alerts Over Time')
st.plotly_chart(fig)

fraud_by_payment_narative = df[df['is_fraud']==1].groupby('payment_narrative').size().reset_index(name='fraud_count')
fraud_by_payment_narative = fraud_by_payment_narative.sort_values(by='fraud_count',ascending=False)
fig1 = px.bar(fraud_by_payment_narative,x='payment_narrative',y='fraud_count',title='fraud by payment narrative')
st.plotly_chart(fig1)