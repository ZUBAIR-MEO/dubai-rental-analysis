# app.py
import streamlit as st
import pandas as pd
import joblib
import os

# Set page config FIRST
st.set_page_config(page_title="Dubai Rent Predictor", layout="centered")

# Load the trained model and metrics
MODEL_PATH = 'rental_price_predictor.pkl'
METRICS_PATH = 'model_metrics.pkl'

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# App UI
st.title("🏢 Dubai Rental Price Predictor")
st.write("🔍 Predict estimated **rent per square foot (AED/sqft)** for a property based on key features.")

# Input fields
version = st.selectbox("Project Version", ['Completed', 'Under Construction'])
area = st.selectbox("Area", ['Downtown Dubai', 'Dubai Marina', 'Business Bay', 'JVC', 'Palm Jumeirah'])  # Adjust as needed
prop_type = st.selectbox("Property Type", ['Apartment', 'Villa'])
sub_type = st.selectbox("Property Sub-Type", ['Studio', '1BR', '2BR', '3BR', 'Penthouse'])  # Simplified

rooms = st.slider("Number of Rooms", min_value=1, max_value=10, value=2)
parking = st.slider("Parking Spaces", min_value=0, max_value=5, value=1)

# Optional area input
actual_area = st.number_input("Actual Area (sq. ft.)", min_value=0.0, format="%.2f")

if st.button("Predict Rent per sq. ft."):
    try:
        input_df = pd.DataFrame([{
            'VERSION_EN': version,
            'AREA_EN': area,
            'PROP_TYPE_EN': prop_type,
            'PROP_SUB_TYPE_EN': sub_type,
            'ROOMS': rooms,
            'PARKING': parking
        }])

        rent_per_sqft = model.predict(input_df)[0]
        st.success(f"🏷️ Predicted Rent: **AED {rent_per_sqft:.2f}/sq. ft.**")

        if actual_area > 0:
            total_rent = rent_per_sqft * actual_area
            st.info(f"💰 Estimated Total Annual Rent: **AED {total_rent:,.2f}**")

    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
