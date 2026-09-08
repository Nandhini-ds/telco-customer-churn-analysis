import joblib

# Load the saved churn prediction pipeline
loaded_pipeline = joblib.load('churn_prediction_pipeline.pkl')

print("Model loaded successfully.")