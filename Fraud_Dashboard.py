import streamlit as st
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Faster Payments Fraud Dashboard")

st.subheader("Welcome to the Fraud Analytics Dashboard. ")
st.markdown("This tool visualizes fraud detection performance and user behavior.")


st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True) 

## KPI 1

uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])
df['date'] = df['payment_timestamp'].dt.date
st.header("📊 Overview Metrics")



col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Transactions", len(df))
col2.metric("Total Value Sent", f"£{df['payment_amount'].sum():,.2f}")
col3.metric(f"Total Fraud Transaction Value",f"£{df[df['is_fraud']==1]['payment_amount'].sum():,.2f}")
col4.metric(f"Total Fraud Alerted Value",f"£{df[df['payment_alerted']==1]['payment_amount'].sum():,.2f}")


# st.markdown(f"Total Fraud Transaction Value £{df[df['is_fraud']==1]['payment_amount'].sum():,.2f}")
# st.markdown(f"Total Fraud Alerted Value £{df[df['payment_alerted']==1]['payment_amount'].sum():,.2f}")

FP = len(df[(df['payment_alerted']==1) & (df['is_fraud']==0)])
FN = len(df[(df['payment_alerted']==0) & (df['is_fraud']==1)])

col1_1,col2_2,col3_3,col4_4 = st.columns(4)
col1_1.metric("Frauds", df["is_fraud"].sum())
col2_2.metric("Alerts Raised", df["payment_alerted"].sum())
col3_3.metric(f"False Positive",FP)
col4_4.metric(f"False Negative",FN)





st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

## KPI 2

st.header("📅 Daily Fraud & Alert Trends")

daily = df.groupby("date").agg(
    frauds=('is_fraud', 'sum'),
    alerts=('payment_alerted', 'sum'),
    txns=('payment_amount', 'count'),
    payment = ('payment_amount', 'sum')

).reset_index()

fig = px.line(daily, x='date', y=['frauds', 'alerts'], title='Frauds and Alerts Over Time')
st.plotly_chart(fig)

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

## KPI 3
st.header("💸 Fraud By Payment Narrative")
fraud_by_payment_narative = df[df['is_fraud']==1].groupby('payment_narrative').agg(fraud_count=('is_fraud','size'),fraud_amount=('payment_amount','sum')).reset_index()
fraud_by_payment_narative = fraud_by_payment_narative.sort_values(by='fraud_count',ascending=False)
fig1 = px.bar(fraud_by_payment_narative,x='payment_narrative',y='fraud_count',color='fraud_amount',title='Fraud by Payment Narrative')
st.plotly_chart(fig1)

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

## KPI 3


st.header("👤 Top Risky Users")

# top_beneficiaries = df[df['is_fraud'] == 1].groupby('beneficiary_id').size().sort_values(ascending=False).head(10).reset_index(name='Fraud Count')
fraud_by_benificiaries = df[df['is_fraud'] == 1].groupby('beneficiary_id').agg(fraud_count=('is_fraud','size'),fraud_amount=('payment_amount','sum')).sort_values(by=['fraud_count','fraud_amount'],ascending=False).head(10).reset_index()
st.subheader("Top Beneficiaries Receiving Fraud")
st.bar_chart(fraud_by_benificiaries,x='beneficiary_id',y=['fraud_count'],color='fraud_amount')

# top_payers = df[df['is_fraud'] == 1].groupby('payer_id').size().sort_values(ascending=False).head(10).reset_index(name='Fraud Count')
top_payers = df[df['is_fraud'] == 1].groupby('payer_id').agg(fraud_count=('is_fraud','size'),fraud_amount=('payment_amount','sum')).sort_values(by=['fraud_count','fraud_amount'],ascending=False).head(10).reset_index()
print(top_payers.head())
st.subheader("Top Payers Sending Fraud")
st.bar_chart(top_payers,x='payer_id',y=['fraud_count'],color='fraud_amount')

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
## KPI 4

TP = len(df[(df['payment_alerted']==1) & (df['is_fraud']==1)])
FP = len(df[(df['payment_alerted']==1) & (df['is_fraud']==0)])
FN = len(df[(df['payment_alerted']==0) & (df['is_fraud']==1)])
TN = len(df[(df['payment_alerted']==0) & (df['is_fraud']==0)])

accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) else 0
precision = TP / (TP + FP) if (TP + FP) else 0
recall = TP / (TP + FN) if (TP + FN) else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0
style = "<style>h2 {text-align: center;}</style>"
st.header("📈 Fraud Model Efficiency Metrics")
col11,col22,col33,col44 = st.columns(4)
col11.metric("Accuracy", f"{accuracy:.2%}")
col22.metric("Precision", f"{precision:.2%}")
col33.metric("Recall", f"{recall:.2%}")
col44.metric("F1 Score", f"{f1:.2%}")

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


## KPI 5

df=df[df['is_fraud'] == 1]
# Count unique payers per beneficiary
payer_counts = df.groupby('beneficiary_id')['payer_id'].nunique().reset_index()
shared_beneficiaries = payer_counts[payer_counts['payer_id'] > 1]['beneficiary_id'].head()

# Filter dataset for only shared beneficiaries
shared_df = df[df['beneficiary_id'].isin(shared_beneficiaries)]

# Group by payer-beneficiary and aggregate payment amount
link_df = shared_df.groupby(['payer_id', 'beneficiary_id'])['payment_amount'].sum().reset_index()
link_df = link_df.sort_values(by='payment_amount',ascending=False)  
# Create node labels
labels = pd.concat([link_df['payer_id'], link_df['beneficiary_id']]).unique().tolist()
label_map = {label: idx for idx, label in enumerate(labels)}

# Map source and target to Sankey indices
sources = link_df['payer_id'].map(label_map).tolist()
targets = link_df['beneficiary_id'].map(label_map).tolist()
values = link_df['payment_amount'].tolist()

# Build Sankey chart
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])

fig.update_layout(title_text="Multiple Payers ➝ Shared Beneficiaries (Fraud)", font_size=12)

# Streamlit render
st.plotly_chart(fig)
