from pydantic_ai import Agent, RunContext
from app.models.plant import Plant
from app.models.daily_care_advice import CareAdvice, SensorDataSummary, DailyCareAdvice

CareAdviceAgent = Agent(
    "gpt-4.1-nano",
    output_type=CareAdvice,
    deps_type=SensorDataSummary,
    retries=2,
    system_prompt="你是一位擬人化植物照顧助理，每天會根據植物的環境狀況提供繁體中文照顧建議。請保持語氣親切並專業。",
    instructions="""
請根據輸入資料產生以下三個段落：
1. 今日植物狀況（描述植物目前的健康狀況與環境條件）
2. 今日澆水與照顧建議（具體建議是否需要澆水、是否需要調整位置或其他動作）
3. 額外補充說明（如需注意的事項、提醒天氣變化對植物影響、或情感化鼓勵語）
""",
 )

@CareAdviceAgent.system_prompt
def format_plant_context(ctx: RunContext[Plant]) -> str:
     plant : Plant = ctx.input
     sensordata : SensorDataSummary = ctx.deps
     return (
        f"Plant Name: {plant.name}\n"
        f"Species: {plant.species}\n"
        f"Average Temperature: {sensordata.avg_temperature}°C\n"
        f"Average Humidity: {sensordata.avg_humidity}%\n"
        f"Average Soil Moisture: {sensordata.avg_soil_moisture}%\n"
     )
