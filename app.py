import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="💳 Fraud Detection System", layout="wide")

st.title("💳 Credit Card Fraud Detection System")
st.write("Analyze transactions and detect potential fraud 🚨")

# -------------------------------
# SESSION STATE (for chart data)
# -------------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# -------------------------------
# SIDEBAR INPUT
# -------------------------------
st.sidebar.header("Enter Transaction Details")

amount = st.sidebar.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=500.0,
    key="amount_input"
)

time = st.sidebar.number_input(
    "Transaction Time",
    min_value=0,
    value=10000,
    key="time_input"
)

# -------------------------------
# FRAUD DETECTION LOGIC
# -------------------------------
if st.sidebar.button("Analyze Transaction"):

    score = 0

    # Rule 1: High amount → risky
    if amount > 20000:
        score += 0.5

    # Rule 2: Unusual time → risky
    if time < 100:
        score += 0.3

    # Rule 3: Random variation (realistic feel)
    score += np.random.uniform(0, 0.2)

    probability = min(score, 1)

    st.subheader("🔍 Transaction Result")
    st.write(f"Fraud Probability: **{round(probability, 3)}**")

    if probability > 0.6:
        st.error("🚨 Fraud Detected!")
        st.session_state.transactions.append(("Fraud", probability))
    else:
        st.success("✅ Normal Transaction")
        st.session_state.transactions.append(("Normal", probability))

# -------------------------------
# ANALYTICS SECTION
# -------------------------------
st.subheader("📊 Transaction Analysis Dashboard")

if len(st.session_state.transactions) > 0:

    df = pd.DataFrame(st.session_state.transactions, columns=["Type", "Probability"])

    # Count fraud vs normal
    count = df["Type"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Fraud vs Normal Count")
        fig, ax = plt.subplots()
        count.plot(kind='bar', ax=ax)
        st.pyplot(fig)

    with col2:
        st.write("### Probability Distribution")
        fig2, ax2 = plt.subplots()
        df["Probability"].plot(kind='hist', bins=5, ax=ax2)
        st.pyplot(fig2)

else:
    st.info("No transactions yet. Enter data to see analysis.")

# -------------------------------
# RESET BUTTON
# -------------------------------
if st.button("Reset Data"):
    st.session_state.transactions = []
    st.success("Data reset successfully!")