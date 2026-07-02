># MedCare Healthcare Application - Complete Setup Guide

## 🎯 Quick Start (Recommended)

### Windows Users
1. Double-click `run.bat` - The script will handle everything automatically!
2. Open your browser and go to `http://127.0.0.1:5000`

### macOS/Linux Users
```bash
chmod +x run.sh
./run.sh
```

---

## 📋 Manual Setup Instructions

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

If you get permission errors, try:
```bash
pip install --user -r requirements.txt
```

### Step 3: Verify Setup

Before running the application, verify everything is set up correctly:

```bash
python verify_setup.py
```

This script will check:
- ✓ Python version
- ✓ Project structure
- ✓ All required files
- ✓ Dependencies installation
- ✓ ML model file
- ✓ Template files

### Step 4: Start the Application

```bash
python main.py
```

You should see:
```
╔════════════════════════════════════════════════════════════╗
║  🏥 MedCare - AI-Powered Healthcare Assessment             ║
║  Institution: Kamaraj College of Engineering and Technology║
╚════════════════════════════════════════════════════════════╝

🚀 Starting server on 127.0.0.1:5000
📝 Debug mode: ON
🔧 Model status: ✓ Loaded

Press Ctrl+C to stop the server
```

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔧 Troubleshooting

### Issue: "Module not found" error

**Solution:** Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Model file not found

**Solution:** Ensure `random_forest_model.pkl` exists in the project root directory

### Issue: Port 5000 already in use

**Solution:** Edit `config.py` and change PORT:
```python
PORT = 5001  # or any other available port
```

### Issue: JavaScript chart not displaying

**Solution:** Clear browser cache and hard refresh (Ctrl+F5 or Cmd+Shift+R)

### Issue: Form submission not working

**Solution:** 
1. Check browser console for errors (F12)
2. Ensure JavaScript is enabled
3. Try a different browser

### Issue: Virtual environment not activating

**Windows:**
```bash
# If activate doesn't work, try:
myenv\Scripts\Activate.ps1
# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📁 Project Structure

```
my_healthcare_app/
│
├── main.py                      # 🚀 Main Flask application
├── model.py                     # 🧠 Model utilities & symptoms
├── config.py                    # ⚙️  Configuration settings
├── verify_setup.py              # ✓ Setup verification script
│
├── requirements.txt             # 📦 Python dependencies
├── README.md                    # 📖 Documentation
├── run.bat                      # ▶️  Auto-run script (Windows)
├── .gitignore                   # 🔒 Git ignore rules
│
├── random_forest_model.pkl      # 🤖 Pre-trained ML model
│
├── static/
│   └── style.css               # 🎨 Global styles
│
└── templates/
    ├── perumale.html           # 🏠 Landing page
    ├── questions.html          # 📝 3-step questionnaire
    └── dashboard.html          # 📊 Results & predictions
```

---

## 🔄 Application Workflow

1. **Landing Page** (`/`)
   - User sees welcome message
   - Click "Start Assessment"

2. **Questionnaire** (`/questions`)
   - Step 1: Personal info (age, gender, medical status)
   - Step 2: Medical history (allergies, medications, family history)
   - Step 3: Symptoms selection

3. **Prediction** (`/predict`)
   - Form submitted via POST
   - Data preprocessed
   - ML model generates prediction
   - Confidence score calculated
   - Risk factors analyzed

4. **Results** (`/dashboard`)
   - Display prediction
   - Show confidence level
   - Visual risk analysis
   - Option to try again or go home

---

## 🎓 Understanding the Application

### Key Components

**main.py**
- Flask application setup
- Route handlers
- Input validation
- Model prediction logic

**model.py**
- Symptom list definitions
- BP mapping
- Utility functions

**config.py**
- Configuration constants
- Default values
- Error messages

### Data Flow

```
User Input (Form)
    ↓
Parse & Validate
    ↓
Convert to Features
    ↓
Preprocess (One-hot encoding, scaling)
    ↓
ML Model Prediction
    ↓
Calculate Confidence
    ↓
Display Results
```

---

## ⚠️ Important Notes

- **Medical Disclaimer**: This application is for educational purposes only. It is NOT a replacement for professional medical advice.
- **Data Privacy**: Do not submit real personal health information unless you understand the privacy implications.
- **Model Accuracy**: Predictions depend on training data quality. Always consult healthcare professionals.
- **Development Only**: This setup is for development/educational purposes. For production, use proper deployment strategies.

---

## 🚀 Deploying to Production

For production deployment:

1. Set `DEBUG = False` in `config.py`
2. Generate a strong `SECRET_KEY`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Set up proper logging
5. Use environment variables for sensitive data
6. Enable HTTPS/SSL
7. Set up database for data persistence
8. Implement proper authentication
9. Add rate limiting
10. Set up monitoring & alerts

Example production run:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

---

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Scikit-learn Docs: https://scikit-learn.org/
- Chart.js Docs: https://www.chartjs.org/

---

## ❓ FAQ

**Q: Can I modify the symptoms list?**
A: Yes, edit `all_symptoms_list` in `model.py`

**Q: How do I train a new model?**
A: Create a training script to train and save with joblib

**Q: Can I use a database?**
A: Yes, integrate Flask-SQLAlchemy or similar ORM

**Q: How do I add user authentication?**
A: Use Flask-Login or Flask-JWT-Extended

**Q: Can I deploy this on Heroku/AWS?**
A: Yes, with appropriate configurations and procfiles

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Run `verify_setup.py`
3. Check browser console (F12)
4. Review Flask debug output
5. Check Python error messages

---

**Happy Coding! 🎉**

*Last Updated: 2024*
*MedCare - Kamaraj College of Engineering and Technology*
