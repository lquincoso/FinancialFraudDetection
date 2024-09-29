from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import os


# Function to safely apply label encoding and handle unseen labels
def safe_transform(encoder, value):
    if hasattr(encoder, 'classes_') and value in encoder.classes_:  # Safely check if encoder has 'classes_'
        return encoder.transform([value])[0]
    else:
        # Handle unseen labels by assigning a new label, like -1
        return -1


# Define the function to load data, preprocess it, and make predictions
def predict_fraud(input_dict):
    # Convert input_dict to a pandas DataFrame
    input_data = pd.DataFrame([input_dict])

    # Load saved model and feature columns
    model_path = os.path.join('model', 'fraud_model.pkl')
    feature_columns_path = os.path.join('model', 'feat_columns.pkl')
    
    rf_model = joblib.load(model_path)
    feature_columns = joblib.load(feature_columns_path)

    # Add the balance change ratio features
    input_data['balance_change_ratio'] = input_data['oldbalanceOrg'] / (input_data['amount'] + 1e-9)
    input_data['remaining_balance_ratio'] = input_data['newbalanceOrig'] / (input_data['oldbalanceOrg'] + 1e-9)

    # Load the saved encoders for nameOrig and nameDest
    le_nameOrig = os.path.join('model', 'le_nameOrig.pkl')
    le_nameDest = os.path.join('model', 'le_nameDest.pkl')

    # Apply label encoding with safe transformation for unseen labels
    input_data['nameOrig'] = safe_transform(le_nameOrig, input_data['nameOrig'][0])
    input_data['nameDest'] = safe_transform(le_nameDest, input_data['nameDest'][0])

    # One-hot encode 'type' column to match training data
    input_data = pd.get_dummies(input_data, columns=['type'], drop_first=True)

    # Ensure the input data has the same columns as during training
    missing_cols = set(feature_columns) - set(input_data.columns)
    for col in missing_cols:
        input_data[col] = 0
    input_data = input_data[feature_columns]

    # Make predictions using the loaded model
    prediction = rf_model.predict(input_data)

    # Output the predictions
    return prediction
