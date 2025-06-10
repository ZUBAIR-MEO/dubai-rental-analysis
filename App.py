# Update the feature importance section in the prediction block:

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
        if hasattr(model.named_steps['regressor'], 'feature_importances_'):
            st.subheader("Feature Importance")
            try:
                # Get numerical feature names
                num_features = list(input_data.columns[9:])  # ACTUAL_AREA, ROOMS, PARKING
                
                # Get categorical feature names after one-hot encoding
                preprocessor = model.named_steps['preprocessor']
                cat_features = []
                
                # Handle categorical features if they exist
                if 'cat' in preprocessor.named_transformers_:
                    ohe = preprocessor.named_transformers_['cat'].named_steps['onehot']
                    cat_features = ohe.get_feature_names_out(input_data.columns[:9])
                
                # Combine all feature names
                all_features = num_features + list(cat_features)
                
                # Get feature importances
                importances = model.named_steps['regressor'].feature_importances_
                
                # Create and display importance dataframe
                importance_df = pd.DataFrame({
                    'Feature': all_features,
                    'Importance': importances
                }).sort_values('Importance', ascending=False)
                
                st.bar_chart(importance_df.set_index('Feature'))
                
            except Exception as e:
                st.warning(f"Could not display feature importance: {str(e)}")
                
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
