import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# -----------------------------
# LOAD MODEL + COLUMNS
# -----------------------------
model = joblib.load("models/fraud_model.pkl")
columns = joblib.load("models/columns.pkl")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.title("💳 Credit Card Fraud Detection System")
st.markdown("### AI-powered banking risk analytics dashboard")

# -----------------------------
# SESSION STATE FOR HISTORY
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# SIDEBAR INPUTS (FIXED KEYS)
# -----------------------------
st.sidebar.header("Transaction Input")

amount = st.sidebar.number_input(
    "Transaction Amount",
    value=100.0,
    key="amount_input"
)

time = st.sidebar.number_input(
    "Transaction Time",
    value=10000.0,
    key="time_input"
)

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("🔍 Analyze Transaction"):

    # Generate fake V1–V28 (since dataset is PCA anonymized)
    random_features = np.random.normal(0, 1, len(columns) - 2)

    # Build input row
    input_data = list(random_features) + [time, amount]

    df = pd.DataFrame([input_data], columns=columns)

    # Prediction
    prob = model.predict_proba(df)[0][1]
    prediction = model.predict(df)[0]

    # Risk level
    if prob < 0.2:
        risk = "LOW"
    elif prob < 0.6:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    status = "FRAUD" if prediction == 1 else "NORMAL"

    # Save history
    st.session_state.history.append({
        "Amount": amount,
        "Time": time,
        "Fraud Probability": round(prob, 4),
        "Risk": risk,
        "Status": status
    })

    # -----------------------------
    # METRICS
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Fraud Probability", f"{prob:.4f}")
    col2.metric("Risk Level", risk)
    col3.metric("Status", status)

    st.markdown("---")

    # -----------------------------
    # PROBABILITY CHART
    # -----------------------------
    st.subheader("📊 Risk Distribution")

    fig, ax = plt.subplots()
    ax.pie(
        [1 - prob, prob],
        labels=["Safe", "Risk"],
        autopct="%1.1f%%",
        colors=["green", "red"]
    )
    st.pyplot(fig)

# -----------------------------
# HISTORY TABLE
# -----------------------------
st.markdown("## 📜 Transaction History")

if len(st.session_state.history) > 0:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(history_df)

    # Download button
    csv = history_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="fraud_report.csv",
        mime="text/csv"
    )

    # -----------------------------
    # ANALYTICS SUMMARY
    # -----------------------------
    st.markdown("## 📊 Analytics Summary")

    total = len(history_df)
    frauds = len(history_df[history_df["Status"] == "FRAUD"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", total)
    col2.metric("Fraud Cases", frauds)
    col3.metric("Fraud %", f"{(frauds/total)*100:.2f}%")

else:
    st.info("No transactions yet. Click Analyze to start simulation.")