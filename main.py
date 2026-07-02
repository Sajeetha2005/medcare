"""
MedCare Flask Application
Healthcare Assessment using AI/ML
"""

import sys
import os

# Ensure console supports unicode on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify
import sqlite3
import joblib
import pandas as pd

# Import model and config
try:
    from model import all_symptoms_list
    print("✓ Model module imported")
except ImportError as e:
    print(f"✗ Error importing model: {e}")
    sys.exit(1)

try:
    from config import *
    print("✓ Config module imported")
except ImportError as e:
    print(f"✗ Error importing config: {e}")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = SECRET_KEY

print(f"✓ Flask app initialized")

# Load model globally
model = None
expected_columns = []

def load_model():
    global model, expected_columns
    try:
        if os.path.exists(MODEL_PATH):
            model, expected_columns = joblib.load(MODEL_PATH)
            print(f"✓ ML model loaded from {MODEL_PATH}")
            return True
        else:
            print(f"⚠ Model file not found: {MODEL_PATH}")
            print(f"  Current directory: {os.getcwd()}")
            return False
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

def init_db():
    """Initialize SQLite database for feedback storage"""
    try:
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("✓ Database initialized (feedback table verified)")
        return True
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        return False

# Load model and initialize database on startup
load_model()
init_db()


def parse_blood_sugar(value):
    """Parse blood sugar value from various formats"""
    try:
        if not value or value == '':
            return DEFAULT_BLOOD_SUGAR
        
        value = str(value).strip()
        
        if '-' in value:
            low, high = map(int, value.split('-'))
            return (low + high) / 2
        elif value.startswith('<'):
            return float(value[1:]) - 1
        elif value.startswith('>'):
            return float(value[1:]) + 1
        else:
            return float(value)
    except Exception as e:
        print(f"⚠ Error parsing blood sugar: {e}")
        return DEFAULT_BLOOD_SUGAR


def preprocess_input(raw_input, expected_columns):
    """Convert raw input to model-ready format"""
    try:
        if not expected_columns:
            raise Exception("Expected columns not available")
            
        df = pd.DataFrame([raw_input])
        df = pd.get_dummies(df)

        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0

        df = df[expected_columns]
        return df
    except Exception as e:
        print(f"⚠ Error preprocessing input: {e}")
        return None


@app.route('/')
def welcome():
    """Home page"""
    try:
        return render_template('perumale.html')
    except Exception as e:
        print(f"✗ Error loading home page: {e}")
        return f"<h1>Error</h1><p>Could not load home page: {str(e)}</p>", 500


@app.route('/questions')
def questions():
    """Questionnaire page"""
    try:
        return render_template('questions.html')
    except Exception as e:
        print(f"✗ Error loading questionnaire: {e}")
        return f"<h1>Error</h1><p>Could not load questionnaire: {str(e)}</p>", 500


@app.route('/predict', methods=['POST'])
def predict():
    """Process prediction request"""
    print("\n" + "="*60)
    print("Processing prediction request...")
    print("="*60)

    try:
        if not model:
            print("✗ Model not available")
            return render_template(
                'dashboard.html',
                prediction="System Error",
                symptoms=[],
                confidence=0,
                smoking=0,
                alcohol=0,
                bp=0,
                sugar=0,
                error="ML Model not loaded. Please restart the application."
            ), 500

        if not expected_columns:
            print("✗ Expected columns not available")
            raise Exception("Model configuration incomplete")

        form_data = request.form.to_dict()
        print(f"✓ Form received: {len(form_data)} fields")

        # Get selected symptoms
        symptoms_selected = request.form.getlist('symptoms[]')
        print(f"✓ Symptoms: {len(symptoms_selected)} selected")

        # Create binary symptom vector
        symptom_vector = {
            symptom: 1 if symptom in symptoms_selected else 0
            for symptom in all_symptoms_list
        }

        # Core features
        input_data = {
            'age': int(form_data.get('age', 0)),
            'gender': form_data.get('gender', 'male'),
            'alcohol': form_data.get('alcohol', 'no'),
            'smoker': form_data.get('smoker', 'no'),
            'blood_sugar': parse_blood_sugar(form_data.get('blood_sugar', '100')),
            'bp_range': form_data.get('bp_range', 'normal')
        }

        # Merge symptoms
        input_data.update(symptom_vector)

        # Preprocess
        input_df = preprocess_input(input_data, expected_columns)
        
        if input_df is None:
            raise Exception("Failed to preprocess input")

        print("✓ Input preprocessed")

        # Prediction
        prediction = model.predict(input_df)[0]
        print(f"✓ Prediction: {prediction}")

        # Confidence
        try:
            probs = model.predict_proba(input_df)[0]
            print(f"  Raw probabilities: {probs}")
            confidence = float(max(probs)) * 100
            print(f"  Calculated confidence: {confidence}")
            
            # Cap at 100 if it exceeds
            if confidence > 100:
                print(f"  Capping confidence from {confidence} to 99.99")
                confidence = 99.99
            
            confidence = round(confidence, 2)
            print(f"✓ Confidence: {confidence}%")
        except Exception as e:
            print(f"  Warning: Could not calculate confidence - {e}")
            confidence = DEFAULT_CONFIDENCE

        # Risk factors
        smoking = 1 if str(form_data.get('smoker', 'no')).lower() == 'yes' else 0
        alcohol = 1 if str(form_data.get('alcohol', 'no')).lower() == 'yes' else 0
        bp = 1 if 'high' in str(form_data.get('bp_range', 'normal')).lower() else 0
        blood_sugar = parse_blood_sugar(form_data.get('blood_sugar', '100'))
        sugar = 1 if blood_sugar > BLOOD_SUGAR_THRESHOLD else 0
        
        # Calculate risk level
        risk_count = smoking + alcohol + bp + sugar
        if risk_count >= 3:
            risk_level = 'High'
            risk_emoji = '🔴'
        elif risk_count >= 1:
            risk_level = 'Moderate'
            risk_emoji = '🟠'
        else:
            risk_level = 'Low'
            risk_emoji = '🟢'

        print("="*60)
        print("✓ Prediction successful\n")

        return render_template(
            'dashboard.html',
            prediction=str(prediction),
            symptoms=list(symptoms_selected[:5]),
            confidence=confidence,
            smoking=int(smoking),
            alcohol=int(alcohol),
            bp=int(bp),
            sugar=int(sugar),
            risk_level=risk_level,
            risk_emoji=risk_emoji,
            error=None
        )

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("="*60 + "\n")
        
        return render_template(
            'dashboard.html',
            prediction="Error",
            symptoms=[],
            confidence=0,
            smoking=0,
            alcohol=0,
            bp=0,
            sugar=0,
            error=f"Error processing prediction: {str(e)}"
        ), 500


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        # Check if request is JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        if not name or not email or not message:
            return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400
            
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
            (name, email, message)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Thank you! Your feedback has been stored.'})
    except Exception as e:
        print(f"✗ Error saving feedback: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while saving your feedback.'}), 500


@app.route('/admin/feedback')
def admin_feedback():
    """Admin dashboard to review feedback"""
    try:
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, email, message, timestamp FROM feedback ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        conn.close()
        
        feedback_list = [
            {'name': row[0], 'email': row[1], 'message': row[2], 'timestamp': row[3]}
            for row in rows
        ]
        return render_template('admin_feedback.html', feedback_list=feedback_list)
    except Exception as e:
        print(f"✗ Error loading feedback reviews: {e}")
        return f"<h1>Error</h1><p>Could not load feedback portal: {str(e)}</p>", 500


@app.errorhandler(404)
def not_found(e):
    return render_template('perumale.html'), 404


@app.errorhandler(500)
def server_error(e):
    return f"<h1>Server Error</h1><p>{str(e)}</p>", 500


if __name__ == '__main__':
    print("\n" + "╔" + "="*58 + "╗")
    print("║  🏥 MedCare - AI Healthcare Assessment System")
    print("║" + " "*58 + "║")
    print(f"║  Starting on: {HOST}:{PORT}")
    print(f"║  Debug Mode: {'ON' if DEBUG else 'OFF'}")
    print(f"║  Model Status: {'✓ Loaded' if model else '✗ Not Loaded'}")
    print("╚" + "="*58 + "╝\n")
    
    try:
        app.run(debug=DEBUG, host=HOST, port=PORT, use_reloader=True)
    except Exception as e:
        print(f"\n✗ Failed to start application: {e}")
        sys.exit(1)