import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model and its preprocessing steps
model = joblib.load("rental_price_predictor.pkl")

st.title("🏠 Rental Price Prediction App")
st.write("Enter the details of the property to predict its monthly rent and rent per square foot.")

# Input fields
area_sqft = st.number_input("Area (sq. ft)", 
                          value=None,
                          placeholder="Enter area in square feet")

bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4])
location = st.selectbox("Location", ['Downtown', 'Marina', 'Jumeirah', 'Business Bay'])
furnished = st.selectbox("Furnishing", ['Furnished', 'Unfurnished', 'Semi-Furnished'])

if st.button("Predict Rent"):
    if area_sqft is None:
        st.error("Please enter the area")
    elif area_sqft <= 0:
        st.error("Area must be a positive number")
    else:
        try:
            # Create input DataFrame with all original features
            input_data = pd.DataFrame({
                'area_sqft': [area_sqft],
                'bedrooms': [bedrooms],
                'bathrooms': [bathrooms],
                'location': [location],
                'furnishing': [furnished]
            })
            
            # Get the expected feature names from the model
            expected_features = model.feature_names_in_
            
            # One-hot encode to match the model's training setup
            input_encoded = pd.get_dummies(input_data)
            
            # Add missing columns with 0 values
            for feature in expected_features:
                if feature not in input_encoded.columns:
                    input_encoded[feature] = 0
            
            # Reorder columns to match training data
            input_encoded = input_encoded[expected_features]
            
            # Make prediction
            predicted_rent = model.predict(input_encoded)[0]
            rent_per_sqft = predicted_rent / area_sqft
            
            st.success(f"🏢 Estimated Monthly Rent: AED {predicted_rent:,.2f}")
            st.info(f"📏 Rent per sq. ft: AED {rent_per_sqft:.2f}")
            
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            st.info("Please ensure all input fields are correctly filled")
