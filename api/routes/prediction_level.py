from fastapi import APIRouter, Depends, HTTPException
from enum import Enum
from model.schema import Description  # Update this import based on your project structure
from functions.prediction_functions import Predict_level

router = APIRouter()

class Tags(Enum):
    predict_result = "Predict Mental Health Level"

@router.post("/predict_level", tags=[Tags.predict_result])
def prediction(input_data: Description):
    return {
        "Mental Health level from 0 - 9": Predict_level(input_data.Description_text)
    }

