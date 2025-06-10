# app.py
import streamlit as st
import pandas as pd
import joblib
import os

# Load the trained model and metrics
MODEL_PATH = 'models/rental_price_predictor.pkl'
METRICS_PATH = 'models/model_metrics.pkl'

@st.cache_resource
def load_model():
    """Load the trained model and metrics"""
    if not os.path.exists(MODEL_PATH):
        st.error("Model not found. Please run the training pipeline first.")
        return None, None
    
    model = joblib.load(MODEL_PATH)
    metrics = joblib.load(METRICS_PATH)
    return model, metrics

model, metrics = load_model()

# App title and description
st.title("🏙️ Dubai Rental Price Predictor")
st.markdown("""
Predict annual rental prices based on property characteristics.
The model was trained on Dubai rental data with the following performance:
""")

# Show model metrics if available
if metrics:
    col1, col2 = st.columns(2)
    col1.metric("R² Score", f"{metrics['r2']:.2f}")
    col2.metric("RMSE", f"AED {metrics['rmse']:,.2f}")

# Input form
with st.form("prediction_form"):
    st.header("Property Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        version = st.selectbox("Version", ["New", "Secondary", "Under Construction"])
        area = st.selectbox("Area", ["Downtown", "Palm Jumeirah", "Jumeirah", "Business Bay"])
        is_freehold = st.selectbox("Freehold", ["Yes", "No"])
        prop_type = st.selectbox("Property Type", ["Apartment", "Villa", "Townhouse"])
        prop_sub_type = st.selectbox("Property Sub-Type", ["Standard", "Deluxe", "Penthouse", "Studio"])
    
    with col2:
        usage = st.selectbox("Usage", ["Residential", "Commercial", "Mixed"])
        nearest_metro = st.selectbox("Nearest Metro", ["Burj Khalifa", "Dubai Mall", "Business Bay", "Palm Jumeirah"])
        nearest_mall = st.selectbox("Nearest Mall", ["Dubai Mall", "Mall of Emirates", "City Walk"])
        nearest_landmark = st.selectbox("Nearest Landmark", ["Burj Khalifa", "Palm Jumeirah", "Dubai Marina"])
        actual_area = st.number_input("Area (sq. ft.)", min_value=300, max_value=10000, value=1200, step=50)
        rooms = st.number_input("Rooms", min_value=0, max_value=10, value=2)
        parking = st.number_input("Parking Spaces", min_value=0, max_value=5, value=1)
    
    submitted = st.form_submit_button("Predict Price")

# Make prediction when form is submitted
if submitted and model:
    input_data = pd.DataFrame({
        'VERSION_EN': [version],
        'AREA_EN': [area],
        'IS_FREE_HOLD_EN': [is_freehold],
        'PROP_TYPE_EN': [prop_type],
        'PROP_SUB_TYPE_EN': [prop_sub_type],
        'USAGE_EN': [usage],
        'NEAREST_METRO_EN': [nearest_metro],
        'NEAREST_MALL_EN': [nearest_mall],
        'NEAREST_LANDMARK_EN': [nearest_landmark],
        'ACTUAL_AREA': [actual_area],
        'ROOMS': [rooms],
        'PARKING': [parking]
    })
    
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Annual Rental Price: **AED {prediction:,.2f}**")
        st.markdown(f"*Approximately **AED {prediction/12:,.2f}** per month*")
        
        # Show feature importance if available
        if hasattr(model.named_steps['regressor'], 'coef_'):
            st.subheader("Feature Importance")
            try:
                # Get feature names after one-hot encoding
                ohe = model.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
                cat_features = ohe.get_feature_names_out(input_data.columns[:9])
                all_features = list(input_data.columns[9:]) + list(cat_features)
                
                # Get coefficients
                coefs = model.named_steps['regressor'].coef_
                importance_df = pd.DataFrame({
                    'Feature': all_features,
                    'Importance': coefs
                }).sort_values('Importance', key=abs, ascending=False)
                
                st.bar_chart(importance_df.set_index('Feature'))
            except Exception as e:
                st.warning(f"Could not display feature importance: {str(e)}")
                
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")

# Add data exploration section
if metrics and st.checkbox("Show sample data"):
    st.subheader("Sample Data Distribution")
    
    # Load sample data (replace with your actual data loading logic)
    try:
        sample_data = pd.read_csv('Dubai_rents_May_2025_cleaned.csv')
        st.dataframe(sample_data.sample(5))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Properties", len(sample_data))
            st.metric("Average Annual Price", f"AED {sample_data['ANNUAL_AMOUNT'].mean():,.2f}")
        with col2:
            st.metric("Most Common Area", sample_data['AREA_EN'].mode()[0])
            st.metric("Most Common Property Type", sample_data['PROP_TYPE_EN'].mode()[0])
    except Exception as e:
        st.warning(f"Could not load sample data: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
**Note**: This application uses a machine learning model trained on historical data.
Actual prices may vary based on market conditions and property specifics.
""")
