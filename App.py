import streamlit as st
import joblib
import pickle
import os
import numpy as np

# -----------------------------
# Define Paths Relative to App
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "rental_price_predictor.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "..", "models", "model_metrics.pkl")

# -----------------------------
# Load Model and Metrics
# -----------------------------
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error(f"Model file not found at {MODEL_PATH}")
    st.stop()

try:
    with open(METRICS_PATH, "rb") as f:
        metrics = pickle.load(f)
except FileNotFoundError:
    st.warning("Metrics file not found. Model performance info unavailable.")
    metrics = {}

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(page_title="🏙️ Dubai Rental Price Predictor", layout="centered")
st.title("🏙️ Dubai Rental Price Predictor")

st.markdown(
    """
    Enter the property details below to estimate:
    - **Monthly Rental Price (AED)**
    - **Rent per Sq. Ft (AED)**
    """
)

# -----------------------------
# Input Form
# -----------------------------
with st.form("input_form"):
    col1, col2 = st.columns(2)

    with col1:
        area_sqft = st.number_input("Area (sq. ft)", min_value=100, max_value=20000, value=1200)
        bedrooms = st.selectbox("Number of Bedrooms", [1, 2, 3, 4, 5])
        bathrooms = st.selectbox("Number of Bathrooms", [1, 2, 3, 4])

    with col2:
        furnishing = st.selectbox("Furnishing", ["Furnished", "Unfurnished", "Partly Furnished"])
        property_type = st.selectbox("Property Type", ["Apartment", "Villa", "Townhouse"])
        location = st.selectbox("Location", ["Downtown", "Marina", "JVC", "Business Bay", "Palm Jumeirah"])

    submitted = st.form_submit_button("🔮 Predict Rental Price")

# -----------------------------
# Prediction Logic
# -----------------------------
def preprocess_input(area, bed, bath, furnish, prop_type, loc):
    """Prepare inputs for prediction."""
    return {
        'area': area,
        'bedrooms': bed,
        'bathrooms': bath,
        'furnishing': furnish,
        'property_type': prop_type,
        'location': loc
    }

if submitted:
    input_data = preprocess_input(area_sqft, bedrooms, bathrooms, furnishing, property_type, location)

    try:
        # Adjust this line if you used a pipeline that includes encoders
        prediction = model.predict([list(input_data.values())])[0]
        rent_per_sqft = prediction / area_sqft

        st.success(f"📦 Estimated Monthly Rent: **AED {prediction:,.2f}**")
        st.info(f"📐 Rent per Sq. Ft: **AED {rent_per_sqft:.2f}**")
    except Exception as e:
        st.error(f"Prediction error: {e}")

# -----------------------------
# Sidebar: Model Metrics
# -----------------------------
st.sidebar.header("📊 Model Performance")
st.sidebar.markdown(f"**R² Score:** {metrics.get('r2', 'N/A'):.2f}")
st.sidebar.markdown(f"**RMSE:** {metrics.get('rmse', 'N/A'):.2f}")
st.sidebar.markdown("---")
st.sidebar.caption("Model trained on Dubai rental market data.\nDeveloped for EU Business School Project.")

