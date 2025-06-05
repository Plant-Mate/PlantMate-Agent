# from pydantic_ai import Agent
# from pydantic_ai import RunContext
# from app.models.plant import Plant
# from app.models.daily_care_advice import Advice, SensorDataSummary, DailyCareAdvice
# from dotenv import load_dotenv
#
# load_dotenv()
# CareAdviceAgent = Agent(
#      "openai:gpt-4.1-nano",
#      input_type=Plant,
#      output_type=Advice,
#      deps_type=SensorDataSummary,
#      retries=2,
#      system_prompt="""
#     You are a plant care assistant. Based on the plant's condition, generate today's care advice.
#     The advice should include:
#      1. Whether the plant needs watering.
#      2. A brief additional note about its current status or environment.
#      """
#  )
#
# @CareAdviceAgent.system_prompt
# def format_plant_context(ctx: RunContext[Plant]) -> str:
#      plant : Plant = ctx.input
#      sensordata : SensorDataSummary = ctx.deps
#      return (
#         f"Plant Name: {plant.name}\n"
#         f"Species: {plant.species}\n"
#         f"Average Temperature: {sensordata.avg_temperature}°C\n"
#         f"Average Humidity: {sensordata.avg_humidity}%\n"
#         f"Average Soil Moisture: {sensordata.avg_soil_moisture}%\n"
#      )
