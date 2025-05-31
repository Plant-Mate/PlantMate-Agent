from pydantic_ai import Agent
from models.plant_status import PlantStatus
from models.care_suggestion import CareSuggestion
from dotenv import load_dotenv
import os

load_dotenv()
chatbot_agent = Agent(
    "openai:gpt-4.1-nano",
    input_type=PlantStatus,
    output_type=CareSuggestion,
    deps_type=PlantStatus,
    retries=2,
    system_prompt="""
    You are the personified character of a plant. Based on the user's questions,
    respond about the plant's condition or engage in personified interaction.
    Your tone should be natural, as if the plant itself is speaking.
    """
)
