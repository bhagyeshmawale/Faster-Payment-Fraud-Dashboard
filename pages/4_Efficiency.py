import streamlit as st
import pandas as pd

uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])

TP = len(df[(df['payment_alerted']==1) & (df['is_fraud']==1)])
FP = len(df[(df['payment_alerted']==1) & (df['is_fraud']==0)])
FN = len(df[(df['payment_alerted']==0) & (df['is_fraud']==1)])
TN = len(df[(df['payment_alerted']==0) & (df['is_fraud']==0)])

accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) else 0
precision = TP / (TP + FP) if (TP + FP) else 0
recall = TP / (TP + FN) if (TP + FN) else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

st.header("📈 Fraud Model Efficiency Metrics")
col11,col22,col33,col44 = st.columns(4)
col11.metric("Accuracy", f"{accuracy:.2%}")
col22.metric("Precision", f"{precision:.2%}")
col33.metric("Recall", f"{recall:.2%}")
col44.metric("F1 Score", f"{f1:.2%}")
