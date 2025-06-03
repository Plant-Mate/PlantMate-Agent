# from pydantic_ai import Agent
# from pydantic_ai import RunContext
# from app.models.plant_status import PlantStatus
# from app.models.care_suggestion import CareSuggestion
# from dotenv import load_dotenv
#
# load_dotenv()
# care_agent = Agent(
#     "openai:gpt-4.1-nano",
#     input_type=PlantStatus,
#     output_type=CareSuggestion,
#     deps_type=PlantStatus,
#     retries=2,
#     system_prompt="""
#     You are a plant care assistant. Based on the plant's condition, generate today's care advice.
#     The advice should include:
#     1. Whether the plant needs watering.
#     2. A brief additional note about its current status or environment.
#     """
# )
#
# @care_agent.system_prompt
# def format_plant_context(ctx: RunContext[PlantStatus]) -> str:
#     plant = ctx.deps
#     return (
#         f"Plant Name: {plant.name}\n"
#         f"Species: {plant.species}\n"
#         f"Days since last watering: {plant.last_watered_days}\n"
#         f"Temperature: {plant.temperature}°C\n"
#         f"Humidity: {plant.humidity}%"
#     )