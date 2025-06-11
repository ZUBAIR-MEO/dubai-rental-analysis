import streamlit as st
import joblib
import pickle
import os
import numpy as np

# --- Load model and metrics safely ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "rental_price_predictor.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "..", "models", "model_metrics.pkl")

# Load model
model = joblib.load(MODEL_PATH)

# Load metrics
with open(METRICS_PATH, "rb") as f:
    metrics = pickle.load(f)

# --- App Title ---
st.set_page_config(page_title="Dubai Rental Predictor", layout="centered")
st.title("🏠 Dubai Rental Price Prediction App")

st.markdown("Enter the property details below to predict the estimated **monthly rental price** and **rent per square foot**.")

# --- Input Fields ---
col1, col2 = st.columns(2)

with col1:
    area_sqft = st.number_input("Area (sq. ft)", min_value=100, max_value=20000, value=1200)
    bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5])
    bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4])

with col2:
    furnishing = st.selectbox("Furnishing", ["Furnished", "Unfurnished", "Partly Furnished"])
    property_type = st.selectbox("Property Type", ["Apartment", "Villa", "Townhouse"])
    location = st.selectbox("Location", ["Downtown", "Marina", "JVC", "Business Bay", "Palm Jumeirah"])

# --- Convert inputs to features ---
def preprocess_input(area, bed, bath, furnish, prop_type, loc):
    # This assumes your model uses one-hot encoding or similar preprocessing
    input_dict = {
        'area': area,
        'bedrooms': bed,
        'bathrooms': bath,
        'furnishing': furnish,
        'property_type': prop_type,
        'location': loc
    }
    return input_dict

# --- Predict Button ---
if st.button("🔮 Predict Rental Price"):
    input_features = preprocess_input(area_sqft, bedrooms, bathrooms, furnishing, property_type, location)
    
    # Convert input to the format your model expects
    # You may need to use a transformer or preprocessor from training
    try:
        # If model includes preprocessing inside pipeline
        prediction = model.predict([list(input_features.values())])[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        st.stop()

    rent_per_sqft = prediction / area_sqft

    st.success(f"📦 Estimated Monthly Rent: **AED {prediction:,.2f}**")
    st.info(f"📐 Rent per Sq. Ft: **AED {rent_per_sqft:.2f}**")

# --- Sidebar: Model Info ---
st.sidebar.header("📊 Model Performance")
st.sidebar.markdown(f"**R² Score**: {metrics.get('r2', 'N/A'):.2f}")
st.sidebar.markdown(f"**RMSE**: {metrics.get('rmse', 'N/A'):.2f}")
st.sidebar.markdown("---")
st.sidebar.markdown("Model powered by joblib & trained using historical Dubai rental listings.")

