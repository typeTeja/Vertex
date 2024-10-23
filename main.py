# Save this as main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

class StudentData(BaseModel):
    code_module: str
    code_presentation: str
    gender: str
    region: str
    highest_education: str
    age_band: str
    num_of_prev_attempts: int
    Student_sum_click: int
    disability: str

# Load the model
try:
    model = joblib.load('student_performance_model.joblib')
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Model file not found. Please ensure the model is trained and saved correctly.")

@app.post("/predict")
def predict(data: StudentData):
    # Convert input data to DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # Make prediction
    try:
        prediction = model.predict(input_df)
        return {"predicted_performance": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model_info")
def model_info():
    return {
        "model_type": "Random Forest Classifier",
        "best_parameters": {
            "max_depth": 10,
            "min_samples_leaf": 4,
            "min_samples_split": 2,
            "n_estimators": 300
        },
        "accuracy": 0.4333,
        "supported_classes": ["Distinction", "Fail", "Pass", "Withdrawn"]
    }

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Student Performance Prediction API is running"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
