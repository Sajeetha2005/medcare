"""
MedCare Application Setup Verification Script
Checks all requirements and dependencies before running the app
"""

import os
import sys

# Ensure console supports unicode on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import importlib
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("📌 Checking Python Version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("   ✓ Python version is compatible\n")
        return True
    else:
        print("   ✗ Python 3.7+ is required\n")
        return False

def check_project_structure():
    """Check if all required files exist"""
    print("📌 Checking Project Structure...")
    
    required_files = {
        'main.py': 'Flask application',
        'model.py': 'Model utilities',
        'config.py': 'Configuration',
        'requirements.txt': 'Dependencies',
        'random_forest_model.pkl': 'ML Model',
        'templates/perumale.html': 'Home template',
        'templates/questions.html': 'Form template',
        'templates/dashboard.html': 'Results template',
        'static/style.css': 'Stylesheet',
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"   ✓ {file_path:<30} ({description})")
        else:
            print(f"   ✗ {file_path:<30} ({description}) - MISSING")
            all_exist = False
    
    print()
    return all_exist

def check_dependencies():
    """Check if all required packages are installed"""
    print("📌 Checking Dependencies...")
    
    required_packages = {
        'flask': 'Flask',
        'pandas': 'pandas',
        'joblib': 'joblib',
        'sklearn': 'scikit-learn',
    }
    
    all_installed = True
    for package, display_name in required_packages.items():
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✓ {display_name:<20} (v{version})")
        except ImportError:
            print(f"   ✗ {display_name:<20} - NOT INSTALLED")
            all_installed = False
    
    print()
    return all_installed

def check_templates():
    """Check if templates have correct structure"""
    print("📌 Checking Template Files...")
    
    templates = [
        'templates/perumale.html',
        'templates/questions.html',
        'templates/dashboard.html',
    ]
    
    all_valid = True
    for template in templates:
        try:
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
                if '<!DOCTYPE html>' in content or '<html' in content:
                    print(f"   ✓ {template:<30} (valid HTML)")
                else:
                    print(f"   ⚠ {template:<30} (might not be HTML)")
        except Exception as e:
            print(f"   ✗ {template:<30} (error: {str(e)})")
            all_valid = False
    
    print()
    return all_valid

def check_model():
    """Check if ML model is loadable"""
    print("📌 Checking ML Model...")
    
    try:
        import joblib
        model_path = 'random_forest_model.pkl'
        
        if Path(model_path).exists():
            try:
                data = joblib.load(model_path)
                print(f"   ✓ Model file found and loadable")
                print(f"   ✓ Model contains {len(data)} items\n")
                return True
            except Exception as e:
                print(f"   ✗ Model file is corrupted: {str(e)}\n")
                return False
        else:
            print(f"   ✗ Model file not found: {model_path}\n")
            return False
    except ImportError:
        print(f"   ✗ joblib not installed\n")
        return False

def generate_report(results):
    """Generate final verification report"""
    print_header("VERIFICATION REPORT")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"✓ Passed: {passed}/{total}")
    print(f"✗ Failed: {failed}/{total}")
    
    if failed == 0:
        print("\n🎉 All checks passed! Application is ready to run.\n")
        print("To start the application, run:")
        print("  python main.py")
        print("\nOr on Windows, double-click: run.bat\n")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.\n")
        if not results['dependencies']:
            print("To install missing dependencies, run:")
            print("  pip install -r requirements.txt\n")
        return False

def main():
    """Run all verification checks"""
    print_header("MedCare Application Verification")
    print("This script will verify that your application is properly set up.\n")
    
    results = {
        'python': check_python_version(),
        'structure': check_project_structure(),
        'templates': check_templates(),
        'dependencies': check_dependencies(),
        'model': check_model(),
    }
    
    success = generate_report(results)
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
