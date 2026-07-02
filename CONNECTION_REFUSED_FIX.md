# 🔴 Connection Refused - Server Not Running

## Issue
Browser shows: **ERR_CONNECTION_REFUSED (-102)**
- This means the Flask server is NOT running or NOT listening on port 5000

## 🔧 Step-by-Step Fix

### Step 1: Install Requirements
Open Command Prompt and run:
```bash
pip install flask pandas joblib scikit-learn
```

### Step 2: Try Simplified App
Run this command:
```bash
python app_simple.py
```

This will show you **exactly what the error is**.

### Step 3: If Still Failing

#### Check what error you get:
```bash
python test_startup.py
```

This diagnostic tool will tell you exactly what's wrong.

#### Common Issues:

**A) Flask not installed**
```bash
pip install flask
```

**B) Port 5000 in use**
Edit `config.py`:
```python
PORT = 5001  # Change to different port
```

**C) Python not in PATH**
- Reinstall Python
- Check "Add Python to PATH"
- Restart computer

**D) Module import errors**
```bash
pip install --upgrade -r requirements.txt
```

## 🚀 Quick Start Commands

Choose ONE and run:

### Option 1: Automated Setup (Recommended)
```
SETUP_AND_RUN.bat
```

### Option 2: Manual Start
```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
python app_simple.py
```

### Option 3: Debug Mode (Shows all errors)
```bash
python app_simple.py
```

### Option 4: Run Diagnostics
```bash
python test_startup.py
```

## 📋 Files Available

| File | Purpose |
|------|---------|
| `SETUP_AND_RUN.bat` | ✓ One-click complete setup |
| `debug_start.bat` | ✓ Debug startup |
| `app_simple.py` | ✓ Simplified Flask app |
| `test_startup.py` | ✓ Diagnostic tool |

## 🎯 Expected Output When Working

If the server starts correctly, you should see:
```
════════════════════════════════════════════════════════════════
🏥 MedCare - AI Healthcare Assessment System
   Starting on: 127.0.0.1:5000
   Debug Mode: ON
   Model Status: ✓ Loaded
════════════════════════════════════════════════════════════════

Press Ctrl+C to stop the server

 * Running on http://127.0.0.1:5000
```

Then open your browser to: `http://127.0.0.1:5000`

## ✅ Checklist

- [ ] Python 3.7+ installed (`python --version`)
- [ ] Flask installed (`pip show flask`)
- [ ] Dependencies installed (`pip show pandas`)
- [ ] Port 5000 available or changed in config.py
- [ ] Model file exists: `random_forest_model.pkl`
- [ ] Templates exist in `templates/` folder
- [ ] No other app running on port 5000

## 🔍 Detailed Troubleshooting

### If you see "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### If you see "Address already in use"
The port is taken. Change it in `config.py`:
```python
PORT = 5001  # or any free port
```

### If you see template errors
Check templates folder exists:
```
templates/
  ├── perumale.html
  ├── questions.html
  └── dashboard.html
```

### If you see model errors
Check model file exists:
```
random_forest_model.pkl
```

## 📞 Still Not Working?

1. Run: `python test_startup.py`
2. Copy all the output
3. Share what errors it shows
4. Check terminal/console for exact error message

---

## 🟢 When It Works

1. You'll see startup message in terminal
2. Browser will load the home page
3. Fill out the form and submit
4. See results on dashboard

**Try:** `SETUP_AND_RUN.bat` first ➜ then open `http://127.0.0.1:5000`
