# 💸 Fast Payment Fraud Detection Dashboard
https://faster-payment-fraud-dashboard.streamlit.app/
This interactive dashboard analyzes synthetic **Faster Payments** transaction data to detect fraud trends, assess rule effectiveness, and improve operational prioritization. Built using **Streamlit**, **Plotly**, and **Pandas**, it enables fraud analysts and data teams to visually monitor fraud KPIs and optimize alert strategies.

---

## 🧩 Features

- 📈 **Monthly Fraud KPIs**: Fraud Rate, False Positive Rate, Value Detection Rate
- 🔍 **Top Risky Beneficiaries**: Detect money mules via payer clustering
- 🧠 **Narrative Analysis**: Analyze suspicious free-text narratives
- 🔀 **Sankey Diagrams**: Visualize payer-to-beneficiary fraud flows
- ⏱️ **Time-based Risk Detection**: Identify fraud-prone hours
- 🧪 **Rule Simulation**: Test new fraud detection rules on historical data
- 📊 **Streamlit Dashboards**: Real-time visualizations for business users

---

## 📁 Dataset Description

Data comes from the `Sample Data` sheet in the assessment workbook and includes:

| Column             | Description                                               |
|--------------------|-----------------------------------------------------------|
| `payment_id`       | Unique identifier for each payment                        |
| `payer_id`         | Customer who initiated the payment                        |
| `beneficiary_id`   | Recipient of the payment                                  |
| `payment_timestamp`| Timestamp of when the payment occurred                    |
| `payment_amount`   | Value of the transaction in GBP                           |
| `payment_alerted`  | Whether the transaction was flagged by fraud rules        |
| `is_fraud`         | Whether the transaction was confirmed as fraudulent       |
| `payment_narrative`| Free-text description entered by the payer (optional)     |

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/bhagyeshmawale/Faster-Payment-Fraud-Dashboard.git

