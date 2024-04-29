from fastapi import APIRouter
from enum import Enum
from model.schema import Description 
from functions.prediction_functions import chatbot_function
import openai
from dotenv import load_dotenv
import os

#AIzaSyDKwOWNBYIXvqmahJuhbxAcyCv8HMtc1ho


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class Tags(Enum):
    predict_result = "Mental Health FAQ Chatbot"


@router.post("/ask_bot", tags=[Tags.predict_result])
def prediction(prompt: Description):
    return {
        "bot's response": chatbot_function(prompt.Description_text)
    }

# OpenAI Chatbot Route
openai.api_key = OPENAI_API_KEY


@router.post("/query_GPT", tags=[Tags.predict_result])
async def query(prompt: Description):
    messages_chat = []
    temparature = 0.5
    max_tokens = 500

    input_prompt = """ " Suppose you are a mental health professional. Now tell me {prompt}"""

    messages_chat.append({"role":"user","content":f"{input_prompt}"})
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages= messages_chat,
        temperature=temparature,
        max_tokens=max_tokens,
    )

    reply = completion.choices[0].message.content
    return reply