import streamlit as st
import pandas as pd
import pickle
import joblib




# Load the trained model
model = joblib.load("models/rental_price_predictor.pkl")

st.title("🏠 Rental Price Prediction App")
st.write("Enter the details of the property to predict its monthly rent and rent per square foot.")

# Example feature inputs — update according to your model features
# Replace or expand this list based on your model input features
area_sqft = st.number_input("Area (sq. ft)", min_value=100, max_value=10000, value=1000)
bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4])
location = st.selectbox("Location", ['Downtown', 'Marina', 'Jumeirah', 'Business Bay'])  # update as needed
furnished = st.selectbox("Furnishing", ['Furnished', 'Unfurnished', 'Semi-Furnished'])

# Create input DataFrame — match this with your model's expected input schema
input_data = pd.DataFrame({
    'area_sqft': [area_sqft],
    'bedrooms': [bedrooms],
    'bathrooms': [bathrooms],
    'location': [location],
    'furnishing': [furnished]
})

# Handle categorical encoding if needed (adjust based on how the model was trained)
# If you used one-hot or label encoding during training, replicate that here
# For example, if you used pandas.get_dummies() during training:
input_data = pd.get_dummies(input_data)

# Align input data with model features (in case some dummies are missing)
model_features = model.feature_names_in_
for col in model_features:
    if col not in input_data.columns:
        input_data[col] = 0
input_data = input_data[model_features]

# Predict
if st.button("Predict Rent"):
    predicted_rent = model.predict(input_data)[0]
    rent_per_sqft = predicted_rent / area_sqft
    st.success(f"🏢 Estimated Monthly Rent: AED {predicted_rent:,.2f}")
    st.info(f"📏 Rent per sq. ft: AED {rent_per_sqft:.2f}")
