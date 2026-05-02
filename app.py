import numpy as np
import streamlit as st

if st.button("Analyze Transaction"):

    score = 0

    # Rule 1: High amount → risky
    if amount > 20000:
        score += 0.5

    # Rule 2: Unusual time (very early transactions)
    if time < 100:
        score += 0.3

    # Rule 3: Add slight randomness (realistic feel)
    score += np.random.uniform(0, 0.2)

    probability = min(score, 1)

    st.write(f"Fraud Probability: {round(probability, 3)}")

    if probability > 0.6:
        st.error("🚨 Fraud Detected!")
        st.session_state.transactions.append(("Fraud", probability))
    else:
        st.success("✅ Normal Transaction")
        st.session_state.transactions.append(("Normal", probability))