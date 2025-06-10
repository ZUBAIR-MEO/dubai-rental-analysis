import streamlit as st
import pandas as pd
import joblib
import os

# Load model
@st.cache_data
def load_models():
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, 'models', 'rental_price_predictor.pkl')

    try:
        rental_model = joblib.load(model_path)
        return {
            'rental': rental_model
        }
    except FileNotFoundError:
        st.error(f"❌ Model file not found at: {model_path}")
        return {}

# Prediction function
def predict_rent(model, features):
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)
    return prediction[0]

# App layout
def main():
    st.set_page_config(page_title="Dubai Rental Price Predictor", layout="centered")
    st.title("🏠 Dubai Rental Price Predictor")
    st.write("Enter the property details below to predict the estimated **monthly rent**.")

    # Load model
    models = load_models()
    if 'rental' not in models:
        st.stop()  # stop app if model not found

    # User input
    location = st.selectbox("Location", ["Downtown", "Marina", "Business Bay", "Jumeirah"])
    bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=2)
    bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
    area = st.number_input("Area (in sqft)", min_value=100, max_value=10000, value=1000)

    if st.button("Predict Rent"):
        features = {
            "location": location,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "area": area
        }

        # One-hot encoding or preprocessing may be needed here depending on model
        try:
            predicted_rent = predict_rent(models['rental'], features)
            st.success(f"💰 Estimated Monthly Rent: AED {predicted_rent:,.2f}")
        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")

if __name__ == "__main__":
    main()
