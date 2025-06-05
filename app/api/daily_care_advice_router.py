from fastapi import APIRouter, Depends
from app.models.daily_care_advice import SensorDataSummary

# from app.services.agents.care_advice_agent import CareAdviceAgent

router = APIRouter(prefix="/api/agents", tags=["agents"])
#
# @router.post("/daily-advice")
# def ask_daily_advice(request: SensorDataSummary, agent: CareAdviceAgent):
#     return {"reply": "Hello World"}
