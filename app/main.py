import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import plant_router, chat_message_router, daily_care_advice_router, demo_router
from app.api.scheduler import generate_daily_care
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
scheduler = BackgroundScheduler()
app = FastAPI()
client_url = os.getenv("DEV_CLIENT_URL", "*")

origins = [
    client_url,
]

app.add_middleware(
    CORSMiddleware, # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(daily_care_advice_router.router)
app.include_router(plant_router.router)
app.include_router(chat_message_router.router)
app.include_router(demo_router.router)

scheduler.add_job(generate_daily_care, 'cron', hour=22, minute=13)

@app.on_event("startup")
def start_scheduler_event():
    scheduler.start()
    print("APScheduler 已啟動")
    atexit.register(lambda: scheduler.shutdown(wait=False))


@app.on_event("shutdown")
def shutdown_scheduler_event():
    scheduler.shutdown(wait=False)
    print("APScheduler 已關閉")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    

