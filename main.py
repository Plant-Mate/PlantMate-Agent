from fastapi import FastAPI
from scheduler import start_scheduler
from api.chatbot import router as chatbot_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    start_scheduler()

app.include_router(chatbot_router, prefix="/api")
