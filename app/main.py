import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import plant_router, chat_message_router, agent_router

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

# app.include_router(agent_router)
app.include_router(plant_router.router)
app.include_router(chat_message_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
