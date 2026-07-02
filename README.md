# MedCare - AI Healthcare Assistant

A Flask-based web application that uses machine learning to predict health conditions based on user symptoms and health factors.

## Features

- 🏥 **Health Assessment**: Multi-step questionnaire collecting symptoms and health data
- 🤖 **AI Predictions**: Machine learning model predicts potential health conditions
- 📊 **Risk Analysis**: Visual representation of health risk factors
- 💯 **Confidence Scores**: Shows prediction confidence percentage
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
my_healthcare_app/
├── main.py                      # Flask application & routes
├── model.py                     # Model utilities & symptom definitions
├── requirements.txt             # Python dependencies
├── random_forest_model.pkl      # Pre-trained ML model
├── static/
│   └── style.css               # Global styles
└── templates/
    ├── perumale.html           # Landing page
    ├── questions.html          # Health questionnaire (3-step form)
    └── dashboard.html          # Results page with predictions
```

## Setup & Installation

### 1. Create Virtual Environment

```bash
python -m venv myenv
```

### 2. Activate Virtual Environment

**On Windows:**
```bash
myenv\Scripts\activate
```

**On macOS/Linux:**
```bash
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The application will start at: `http://127.0.0.1:5000`

## Usage

1. **Home Page** - Click "Start Assessment" to begin
2. **Step 1** - Enter personal information (name, age, gender, etc.)
3. **Step 2** - Provide medical history (allergies, medications, family history, etc.)
4. **Step 3** - Select symptoms and consent to data usage
5. **Results** - View AI prediction, confidence score, and risk analysis

## API Endpoints

- `GET /` - Home/Welcome page
- `GET /questions` - Health questionnaire page
- `POST /predict` - Process form and return prediction results

## Troubleshooting

### Model Not Loading
- Ensure `random_forest_model.pkl` exists in the project root
- Check that the model file is not corrupted

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
Edit `main.py` and change the port:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

## Technologies Used

- **Backend**: Flask (Python)
- **ML Library**: scikit-learn
- **Data Processing**: pandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js

## Important Disclaimer

⚠️ **This application is for educational purposes only.** It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider before making any health decisions.

## Authors

- Sajeetha R
- Kamaraj College of Engineering and Technology

## License

This project is for educational use at Kamaraj College of Engineering and Technology.
