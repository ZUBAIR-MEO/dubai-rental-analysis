# dubai_rental_data_pipeline.py
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import SQLAlchemyError
import smtplib
from email.mime.text import MIMEText
import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dubai_rental_pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

MODELS_DIR = 'models'
os.makedirs(MODELS_DIR, exist_ok=True)

def send_email_alert(subject, body):
    """Send an alert email using Gmail SMTP."""
    load_dotenv(override=True)
    SENDER_EMAIL = os.getenv("EMAIL_SENDER")
    RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        logging.info("✅ Alert email sent successfully.")
    except Exception as e:
        logging.error(f"❌ Failed to send alert email: {e}")

def clean_data():
    """Load and clean the Dubai rental data."""
    try:
        # Load dataset
        file_path = 'Dubai rents-May 2025.csv'
        df = pd.read_csv(file_path)

        logging.info("Initial data preview:")
        logging.info(df.head())

        # Remove specific columns if they exist
        columns_to_remove = ['TOTAL_PROPERTIES', 'START_DATE', 'END_DATE']
        logging.info(f"\nRemoving specific columns: {columns_to_remove}")
        df.drop(columns=[col for col in columns_to_remove if col in df.columns], inplace=True)

        # Drop rows where all values are missing
        initial_count = len(df)
        df.dropna(how='all', inplace=True)
        cleaned_count = len(df)
        
        if initial_count != cleaned_count:
            logging.info(f"Removed {initial_count - cleaned_count} completely empty rows")

        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        # Save cleaned data to new CSV file
        cleaned_file_path = 'Dubai_rents_May_2025_cleaned.csv'
        df.to_csv(cleaned_file_path, index=False)
        logging.info(f"\nCleaned data saved to: {cleaned_file_path}")
        
        # Log missing values after cleaning
        logging.info("\nMissing values after cleaning:")
        logging.info(df.isnull().sum())
        
        return cleaned_file_path

    except Exception as e:
        logging.error(f"❌ Data cleaning failed: {str(e)}")
        send_email_alert(
            subject="Data Cleaning Failure: Dubai Rental Analysis",
            body=f"Data cleaning process failed with error:\n{str(e)}"
        )
        raise

def train_rental_model(data_path):
    """Train and save a linear regression model for rental price prediction."""
    try:
        df = pd.read_csv(data_path)
        
        # Identify features and target based on your columns
        categorical_features = [
            'VERSION_EN', 
            'AREA_EN', 
            'IS_FREE_HOLD_EN',
            'PROP_TYPE_EN',
            'PROP_SUB_TYPE_EN',
            'USAGE_EN',
            'NEAREST_METRO_EN',
            'NEAREST_MALL_EN',
            'NEAREST_LANDMARK_EN'
        ]
        
        numerical_features = [
            'ACTUAL_AREA',
            'ROOMS',
            'PARKING'
        ]
        
        # Target variable
        target = 'ANNUAL_AMOUNT'
        
        # Preprocessing pipeline
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # Create and train model pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])
        
        # Split data - first drop rows where target is missing
        df = df.dropna(subset=[target])
        X = df[categorical_features + numerical_features]
        y = df[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=0.2, 
            random_state=42
        )
        
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        logging.info(f"Model evaluation metrics:")
        logging.info(f"RMSE: {rmse:.2f}")
        logging.info(f"R2 Score: {r2:.2f}")
        
        # Save model
        model_path = os.path.join(MODELS_DIR, 'rental_price_predictor.pkl')
        joblib.dump(model, model_path)
        logging.info(f"Model saved to {model_path}")
        
        # Save evaluation metrics
        metrics = {
            'rmse': rmse,
            'r2': r2,
            'features_used': categorical_features + numerical_features,
            'target': target
        }
        joblib.dump(metrics, os.path.join(MODELS_DIR, 'model_metrics.pkl'))
        
        return model_path
        
    except Exception as e:
        logging.error(f"❌ Model training failed: {str(e)}")
        send_email_alert(
            subject="Model Training Failure: Dubai Rental Analysis",
            body=f"Model training failed with error:\n{str(e)}"
        )
        raise

def load_to_postgres(cleaned_file_path):
    """Load cleaned data into PostgreSQL database."""
    try:
        load_dotenv()
        connection_url = URL.create(
            drivername="postgresql",
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME')
        )

        engine = create_engine(connection_url)

        with engine.begin() as connection:
            logging.info("✅ PostgreSQL connection successful!")

            df = pd.read_csv(cleaned_file_path)

            logging.info(f"Total records to import: {len(df)}")

            df.to_sql(
                "property_data",
                connection,
                if_exists="replace",
                index=False,
                method='multi'
            )

            success_msg = f"Successfully imported {len(df)} records to PostgreSQL!"
            logging.info(f"✅ {success_msg}")

            send_email_alert(
                subject="Data Load Success: Dubai Rental Analysis",
                body=success_msg
            )

    except SQLAlchemyError as e:
        error_msg = f"Transaction failed. SQLAlchemy error details:\n{str(e)}"
        logging.error(f"❌ {error_msg}")
        send_email_alert(
            subject="Data Load Failure: Dubai Rental Analysis",
            body=error_msg
        )
        raise
    except Exception as e:
        error_msg = f"Unexpected error occurred:\n{str(e)}"
        logging.error(f"❌ {error_msg}")
        send_email_alert(
            subject="Data Load Failure: Dubai Rental Analysis",
            body=error_msg
        )
        raise
    finally:
        if 'engine' in locals():
            engine.dispose()

def main():
    """Main function to run the data pipeline."""
    try:
        logging.info("Starting Dubai rental data pipeline...")
        
        # Step 1: Clean the data
        cleaned_file = clean_data()
        
        # Step 2: Train model
        model_path = train_rental_model(cleaned_file)
        
        # Step 3: Load to PostgreSQL
        load_to_postgres(cleaned_file)
        
        logging.info("✅ Pipeline completed successfully!")
        
    except Exception as e:
        logging.error(f"❌ Pipeline failed: {str(e)}")
        send_email_alert(
            subject="Pipeline Failure: Dubai Rental Analysis",
            body=f"The data pipeline failed with error:\n{str(e)}"
        )

if __name__ == "__main__":
    main()