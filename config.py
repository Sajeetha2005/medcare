"""
Configuration file for MedCare Healthcare Application
"""

# Flask Configuration
FLASK_ENV = 'development'
DEBUG = True
HOST = '127.0.0.1'
PORT = 5000
SECRET_KEY = 'your-secret-key-change-this-in-production'

# Model Configuration
MODEL_PATH = 'random_forest_model.pkl'
DEFAULT_CONFIDENCE = 85

# Blood Sugar Defaults
DEFAULT_BLOOD_SUGAR = 100
BLOOD_SUGAR_THRESHOLD = 140  # mg/dL

# Risk Factor Mapping
RISK_FACTORS = {
    'smoking': 'Smoking Status',
    'alcohol': 'Alcohol Consumption',
    'bp': 'Blood Pressure',
    'sugar': 'Blood Sugar Level'
}

# Application Info
APP_NAME = 'MedCare'
APP_DESCRIPTION = 'AI-Powered Healthcare Assessment'
INSTITUTION = 'Kamaraj College of Engineering and Technology'

# Error Messages
ERROR_MODEL_NOT_FOUND = 'Machine learning model not found. Please ensure random_forest_model.pkl is in the project root.'
ERROR_INVALID_INPUT = 'Invalid input received. Please check your form data.'
ERROR_PROCESSING = 'An error occurred while processing your request.'
ERROR_MODEL_PREDICTION = 'Could not generate prediction. Please try again.'

# Info Messages
SUCCESS_PREDICTION = 'Prediction generated successfully!'
SUCCESS_LOAD = 'Application loaded successfully!'
