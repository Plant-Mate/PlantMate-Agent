from pydantic_ai import Agent
from app.models.plant_status import PlantStatus
from app.models.daily_care_advice import Advice, SensorDataSummary, DailyCareAdvice
from dotenv import load_dotenv

load_dotenv()
ChatbotAgent = Agent(
    "openai:gpt-4.1-nano",
    input_type=PlantStatus,
    output_type=Advice,
    deps_type=PlantStatus,
    retries=2,
    system_prompt="""
    You are the personified character of a plant. Based on the user's questions,
    respond about the plant's condition or engage in personified interaction.
    Your tone should be natural, as if the plant itself is speaking.
    """
)
