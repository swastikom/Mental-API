from fastapi import FastAPI
from routes.prediction import router as prediction_router
from routes.chatbot import router as chatbot_router
from routes.prediction_level import router as prediction_level_router
from routes.tips import router as tips_router
from routes.clinics import router as clinic_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # Add your frontend's origin here
    "https://medeasy.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)
app.include_router(prediction_level_router)
app.include_router(tips_router)
app.include_router(chatbot_router)
app.include_router(clinic_router)