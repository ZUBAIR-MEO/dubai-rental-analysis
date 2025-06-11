import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model
model = joblib.load("rental_price_predictor.pkl")

st.title("🏠 Rental Price Prediction App")
st.write("Enter the details of the property to predict its monthly rent and rent per square foot.")

# Input fields with no default value and full range
area_sqft = st.number_input("Area (sq. ft)", 
                           value=None,  # No default value
                           min_value=-np.inf, 
                           max_value=np.inf,
                           step=1.0,
                           format="%f",
                           placeholder="Enter area in square feet")

bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4])
location = st.selectbox("Location", ['Downtown', 'Marina', 'Jumeirah', 'Business Bay'])
furnished = st.selectbox("Furnishing", ['Furnished', 'Unfurnished', 'Semi-Furnished'])

# Create input DataFrame only when area is provided
if area_sqft is not None:
    input_data = pd.DataFrame({
        'area_sqft': [area_sqft],
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'location': [location],
        'furnishing': [furnished]
    })

    # One-hot encode categorical variables
    input_data = pd.get_dummies(input_data)

    # Align input data with model features
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[model_features]

# Predict with validation
if st.button("Predict Rent"):
    if area_sqft is None:
        st.error("Please enter the area")
    elif area_sqft <= 0:
        st.error("Area must be a positive number")
    else:
        try:
            predicted_rent = model.predict(input_data)[0]
            rent_per_sqft = predicted_rent / area_sqft
            st.success(f"🏢 Estimated Monthly Rent: AED {predicted_rent:,.2f}")
            st.info(f"📏 Rent per sq. ft: AED {rent_per_sqft:.2f}")
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")
