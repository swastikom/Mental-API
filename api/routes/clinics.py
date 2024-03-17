from fastapi import APIRouter
from model.schema import Description 
from enum import Enum
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

router = APIRouter()

class Tags(Enum):
    nearest_mental_health_clinic = "Mental Health Clinics near Kolkata"

@router.post("/mental_health_clinics", tags=[Tags.nearest_mental_health_clinic])
def get_mental_health_clinics(place_name: Description):
    genai.configure(api_key=f"{GEMINI_API_KEY}")

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
    {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

    convo = model.start_chat(history=[])

    convo.send_message(f"List of Mental health clinics in {place_name} from Google Map in real time with Mental Health clinic name, address, website and phone number in JSON format")
    data = convo.last.text
    output_string = data[8:-3]
    
    print(output_string)
    print(type(output_string))
    json_data =  json.loads(output_string)

    return json_data






