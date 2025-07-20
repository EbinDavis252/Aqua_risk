import streamlit as st
import pandas as pd
import sqlite3
import pickle
from datetime import datetime

# --- Load Trained Models ---
with open('ml_models/financial_model.pkl', 'rb') as f:
    financial_model = pickle.load(f)

with open('ml_models/technical_model.pkl', 'rb') as f:
    technical_model = pickle.load(f)

# --- SQLite Connection ---
conn = sqlite3.connect('database/aqua_risk.db')
c = conn.cursor()

# --- Utility Functions ---
def predict_financial_risk(data):
    return financial_model.predict_proba([data])[0][1]  # Probability of default

def predict_technical_risk(data):
    return technical_model.predict_proba([data])[0][1]  # Probability of farm failure

def save_to_database(farmer_id, financial_risk, technical_risk):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("""
        INSERT INTO model_outputs (farmer_id, financial_risk, technical_risk, result_time)
        VALUES (?, ?, ?, ?)
    """, (farmer_id, financial_risk, technical_risk, now))
    conn.commit()

# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="Aqua Loan Risk Assessment")

st.title("🌊 AI-Driven Risk Assessment System for Aqua Loan Providers")
st.markdown("Assess both **Loan Default Risk** and **Fish Farm Failure Risk** using AI/ML models.")

tab1, tab2, tab3 = st.tabs(["🧾 Risk Assessment Form", "📈 Risk Prediction", "📋 Past Risk Logs"])

# --- Tab 1: Input Form ---
with tab1:
    st.subheader("🧾 Enter Farmer & Farm Details")

    # Farmer Input
    farmer_id = st.text_input("Farmer ID")
    age = st.slider("Age", 18, 70, 35)
    income = st.number_input("Monthly Income (INR)", 1000, 200000, 50000)
    loan_amount = st.number_input("Loan Amount (INR)", 1000, 500000, 80000)
    region = st.selectbox("Region", ['Andhra', 'TamilNadu', 'Kerala', 'Karnataka'])
    loan_term = st.slider("Loan Term (months)", 3, 36, 12)
    previous_default = st.selectbox("Previous Default?", ['No', 'Yes'])
    farm_type = st.selectbox("Farm Type", ['Freshwater', 'Brackish'])

    # Water Quality Inputs
    st.subheader("🌊 Enter Water Quality Parameters")
    temp = st.slider("Water Temperature (°C)", 20, 40, 28)
    pH = st.slider("pH Level", 5.0, 9.0, 7.5)
    ammonia = st.slider("Ammonia Level (mg/L)", 0.0, 5.0, 0.5)
    DO = st.slider("Dissolved Oxygen (mg/L)", 1.0, 10.0, 5.0)
    turbidity = st.slider("Turbidity (NTU)", 0, 10, 3)

    if st.button("🔍 Predict Risk"):
        st.session_state.run_model = True
        st.session_state.inputs = {
            "farmer_id": farmer_id, "age": age, "income": income, "loan_amount": loan_amount,
            "region": region, "loan_term": loan_term, "previous_default": previous_default,
            "farm_type": farm_type, "temp": temp, "pH": pH, "ammonia": ammonia,
            "DO": DO, "turbidity": turbidity
        }

# --- Tab 2: Prediction & Result ---
with tab2:
    if st.session_state.get("run_model", False):
        inputs = st.session_state.inputs

        # Encode inputs
        region_map = {'Andhra': 0, 'TamilNadu': 1, 'Kerala': 2, 'Karnataka': 3}
        farm_map = {'Freshwater': 0, 'Brackish': 1}
        prev_def = 1 if inputs['previous_default'] == 'Yes' else 0

        financial_input = [
            inputs['age'], inputs['income'], inputs['loan_amount'],
            region_map[inputs['region']], inputs['loan_term'], prev_def,
            farm_map[inputs['farm_type']]
        ]

        technical_input = [inputs['temp'], inputs['pH'], inputs['ammonia'], inputs['DO'], inputs['turbidity']]

        # Predict
        fin_risk = round(predict_financial_risk(financial_input), 3)
        tech_risk = round(predict_technical_risk(technical_input), 3)

        st.success("✅ Risk Predictions Completed")
        st.metric("💼 Loan Default Risk", f"{fin_risk * 100:.1f}%")
        st.metric("🌊 Farm Failure Risk", f"{tech_risk * 100:.1f}%")

        # Save to DB
        save_to_database(inputs['farmer_id'], fin_risk, tech_risk)

# --- Tab 3: View Logs ---
with tab3:
    st.subheader("📋 Risk Assessment Logs")
    logs_df = pd.read_sql_query("SELECT * FROM model_outputs ORDER BY result_time DESC", conn)
    st.dataframe(logs_df, use_container_width=True)

