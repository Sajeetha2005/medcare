"""
MedCare Flask Application - Simplified Version
This is a minimal version to ensure the app starts
"""

import sys
import os

print("\n" + "="*70)
print("MedCare Application - Starting...")
print("="*70 + "\n")

# Step 1: Try importing Flask
print("[1/5] Importing Flask...")
try:
    from flask import Flask, render_template, request, jsonify
    import sqlite3
    print("     ✓ Flask and sqlite3 imported\n")
except ImportError as e:
    print(f"     ✗ ERROR: {e}")
    print("     Install Flask: pip install Flask\n")
    sys.exit(1)

# Step 2: Try importing other libraries
print("[2/5] Importing dependencies...")
try:
    import joblib
    import pandas as pd
    print("     ✓ Dependencies imported\n")
except ImportError as e:
    print(f"     ✗ ERROR: {e}")
    print("     Install dependencies: pip install -r requirements.txt\n")
    sys.exit(1)

# Step 3: Try importing custom modules
print("[3/5] Loading custom modules...")
try:
    from model import all_symptoms_list
    print("     ✓ Model module loaded")
    from config import DEBUG, HOST, PORT, MODEL_PATH
    print("     ✓ Config loaded\n")
except Exception as e:
    print(f"     ✗ ERROR: {e}\n")
    sys.exit(1)

# Step 4: Create Flask app
print("[4/5] Creating Flask app...")
app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = 'dev-key'
print("     ✓ Flask app created\n")

# Step 5: Load ML model (optional - app works without it)
print("[5/5] Loading ML model...")
model = None
expected_columns = []

if os.path.exists(MODEL_PATH):
    try:
        model, expected_columns = joblib.load(MODEL_PATH)
        print(f"     ✓ Model loaded ({os.path.getsize(MODEL_PATH)} bytes)\n")
    except Exception as e:
        print(f"     ⚠ Could not load model: {e}")
        print(f"     ⚠ App will work but predictions disabled\n")
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
        print("     ✓ Database initialized (feedback table verified)\n")
    except Exception as e:
        print(f"     ✗ Database initialization error: {e}\n")

init_db()

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home page"""
    try:
        return render_template('perumale.html')
    except Exception as e:
        return f"<h1>Error</h1><p>Home page error: {str(e)}</p>", 500


@app.route('/questions')
def questions():
    """Questions page"""
    try:
        return render_template('questions.html')
    except Exception as e:
        return f"<h1>Error</h1><p>Questions page error: {str(e)}</p>", 500


@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        if not model:
            return render_template(
                'dashboard.html',
                prediction="Model not loaded",
                symptoms=[],
                confidence=0,
                smoking=0,
                alcohol=0,
                bp=0,
                sugar=0,
                error="ML model is not available"
            ), 500

        # Get form data
        form_data = request.form.to_dict()
        symptoms_selected = request.form.getlist('symptoms[]')

        # Create symptom vector
        symptom_vector = {
            symptom: 1 if symptom in symptoms_selected else 0
            for symptom in all_symptoms_list
        }

        # Prepare input
        input_data = {
            'age': int(form_data.get('age', 0)),
            'gender': form_data.get('gender', 'male'),
            'alcohol': form_data.get('alcohol', 'no'),
            'smoker': form_data.get('smoker', 'no'),
            'blood_sugar': float(form_data.get('blood_sugar', 100)),
            'bp_range': form_data.get('bp_range', 'normal')
        }
        input_data.update(symptom_vector)

        # Preprocess
        df = pd.DataFrame([input_data])
        df = pd.get_dummies(df)
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns]

        # Predict
        prediction = model.predict(df)[0]
        try:
            confidence = int(round(max(model.predict_proba(df)[0]) * 100))
        except:
            confidence = 85

        # Extract risk factors
        smoking = 1 if str(form_data.get('smoker', 'no')).lower() == 'yes' else 0
        alcohol = 1 if str(form_data.get('alcohol', 'no')).lower() == 'yes' else 0
        bp = 1 if 'high' in str(form_data.get('bp_range', 'normal')).lower() else 0
        sugar = 1 if float(form_data.get('blood_sugar', 100)) > 140 else 0

        return render_template(
            'dashboard.html',
            prediction=str(prediction),
            symptoms=list(symptoms_selected[:5]),
            confidence=int(confidence),
            smoking=int(smoking),
            alcohol=int(alcohol),
            bp=int(bp),
            sugar=int(sugar),
            error=None
        )

    except Exception as e:
        return render_template(
            'dashboard.html',
            prediction="Error",
            symptoms=[],
            confidence=0,
            smoking=0,
            alcohol=0,
            bp=0,
            sugar=0,
            error=f"Error: {str(e)}"
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


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('perumale.html'), 404


@app.errorhandler(500)
def server_error(e):
    return f"<h1>500 Error</h1><p>{str(e)}</p>", 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print(f"🚀 MedCare Application Starting")
    print(f"   URL: http://{HOST}:{PORT}")
    print(f"   Debug: {DEBUG}")
    print(f"   Model: {'✓ Loaded' if model else '✗ Not loaded'}")
    print("="*70)
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)
    except Exception as e:
        print(f"\n✗ Failed to start: {e}")
        sys.exit(1)
