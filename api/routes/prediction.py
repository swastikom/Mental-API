from fastapi import APIRouter
from enum import Enum
from model.schema import Description  # Update this import based on your project structure
from functions.prediction_functions import predict_emotion,suicide_text_indicator,stress_prediction

router = APIRouter()

class Tags(Enum):
    predict_result = "Predict Result"

@router.get('/', tags=['Home'])
def home():
    return {"message": "Let's Predict the Mental Health Level."}

@router.post("/predict_emotion", tags=[Tags.predict_result])
def prediction(input_data: Description):
    return {
        "Emotion Predicted": predict_emotion(input_data.Description_text)
    }

@router.post("/predict_suicidal_text", tags=[Tags.predict_result])
def prediction(input_data: Description):
    return {
        "Suicide text Predicted": suicide_text_indicator(input_data.Description_text)
    }

@router.post("/predict_stress", tags=[Tags.predict_result])
def prediction(input_data: Description):
    return {
        "Stress Prediction": stress_prediction(input_data.Description_text)
    }