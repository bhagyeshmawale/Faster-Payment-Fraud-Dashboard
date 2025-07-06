import streamlit as st
import pandas as pd
import plotly.graph_objects as go

uploaded_file = "transactions.xlsx"
df = pd.read_excel(uploaded_file, sheet_name="Sample Data", parse_dates=['payment_timestamp'])


df=df[df['is_fraud'] == 1]
# Count unique payers per beneficiary
payer_counts = df.groupby('beneficiary_id')['payer_id'].nunique().reset_index()
shared_beneficiaries = payer_counts[payer_counts['payer_id'] > 1]['beneficiary_id'].head()

# Filter dataset for only shared beneficiaries
shared_df = df[df['beneficiary_id'].isin(shared_beneficiaries)]

# Group by payer-beneficiary and aggregate payment amount
link_df = shared_df.groupby(['payer_id', 'beneficiary_id'])['payment_amount'].sum().reset_index()

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

fig.update_layout(title_text="Multiple Payers ➝ Shared Beneficiaries (Sankey)", font_size=12)

# Streamlit render
st.plotly_chart(fig)
