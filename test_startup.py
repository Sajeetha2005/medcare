#!/usr/bin/env python3
"""
MedCare Application Startup Diagnostic Script
Run this to test if the application can start properly
"""

import sys
import os

# Ensure console supports unicode on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def test_imports():
    """Test if all modules can be imported"""
    print("="*60)
    print("Testing Module Imports...")
    print("="*60 + "\n")
    
    tests = [
        ("Flask", "flask"),
        ("pandas", "pandas"),
        ("joblib", "joblib"),
        ("scikit-learn", "sklearn"),
    ]
    
    all_pass = True
    for name, module_name in tests:
        try:
            __import__(module_name)
            print(f"✓ {name:<20} OK")
        except ImportError as e:
            print(f"✗ {name:<20} FAILED: {e}")
            all_pass = False
    
    print()
    return all_pass


def test_files():
    """Test if all required files exist"""
    print("="*60)
    print("Testing Required Files...")
    print("="*60 + "\n")
    
    files = [
        'main.py',
        'model.py',
        'config.py',
        'requirements.txt',
        'random_forest_model.pkl',
        'templates/perumale.html',
        'templates/questions.html',
        'templates/dashboard.html',
        'static/style.css',
    ]
    
    all_pass = True
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✓ {file_path:<40} Found")
        else:
            print(f"✗ {file_path:<40} MISSING")
            all_pass = False
    
    print()
    return all_pass


def test_config():
    """Test if config can be loaded"""
    print("="*60)
    print("Testing Configuration...")
    print("="*60 + "\n")
    
    try:
        from config import DEBUG, HOST, PORT, MODEL_PATH, APP_NAME
        print(f"✓ Config imported successfully")
        print(f"  - APP_NAME: {APP_NAME}")
        print(f"  - DEBUG: {DEBUG}")
        print(f"  - HOST: {HOST}")
        print(f"  - PORT: {PORT}")
        print(f"  - MODEL_PATH: {MODEL_PATH}")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to load config: {e}\n")
        return False


def test_model_module():
    """Test if model module can be loaded"""
    print("="*60)
    print("Testing Model Module...")
    print("="*60 + "\n")
    
    try:
        from model import all_symptoms_list
        print(f"✓ Model module imported")
        print(f"  - Symptoms defined: {len(all_symptoms_list)}")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to load model module: {e}\n")
        return False


def test_model_file():
    """Test if ML model can be loaded"""
    print("="*60)
    print("Testing ML Model File...")
    print("="*60 + "\n")
    
    try:
        import joblib
        from config import MODEL_PATH
        
        if not os.path.exists(MODEL_PATH):
            print(f"✗ Model file not found: {MODEL_PATH}")
            print(f"  Current directory: {os.getcwd()}")
            print()
            return False
        
        try:
            data = joblib.load(MODEL_PATH)
            print(f"✓ Model file loaded successfully")
            print(f"  - File size: {os.path.getsize(MODEL_PATH)} bytes")
            print(f"  - Model contains: {len(data)} items")
            print()
            return True
        except Exception as e:
            print(f"✗ Model file corrupted or unreadable: {e}\n")
            return False
    except Exception as e:
        print(f"✗ Error testing model: {e}\n")
        return False


def test_flask_app():
    """Test if Flask app can be created"""
    print("="*60)
    print("Testing Flask Application...")
    print("="*60 + "\n")
    
    try:
        from main import app, model
        print(f"✓ Flask app created successfully")
        print(f"  - Debug mode: {app.debug}")
        print(f"  - Model loaded: {'Yes' if model else 'No'}")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to create Flask app: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║ MedCare Application Startup Diagnostics")
    print("╚" + "="*58 + "╝")
    print()
    
    results = {
        'Imports': test_imports(),
        'Files': test_files(),
        'Config': test_config(),
        'Model Module': test_model_module(),
        'Model File': test_model_file(),
        'Flask App': test_flask_app(),
    }
    
    print("="*60)
    print("Diagnostic Results")
    print("="*60 + "\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed\n")
    
    if passed == total:
        print("🎉 All checks passed! Application should run fine.")
        print("\nTo start the application, run:")
        print("  python main.py\n")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.\n")
        
        failed_tests = [k for k, v in results.items() if not v]
        print("Failed tests:")
        for test in failed_tests:
            print(f"  - {test}")
        print()
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
