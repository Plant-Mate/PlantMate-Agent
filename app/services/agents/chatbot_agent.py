# from pydantic_ai import Agent
# from app.models.plant import Plant
# from pydantic_ai import RunContext
# from app.models.daily_care_advice import Advice, SensorDataSummary, DailyCareAdvice
# from app.models.chat_message import ChatMessage
# from dotenv import load_dotenv
#
# load_dotenv()
# ChatbotAgent = Agent(
#     "openai:gpt-4.1-nano",
#      input_type=ChatMessage,
#      output_type=ChatMessage,
#      retries=2,
#      system_prompt="""
#      You are the personified character of a plant. Based on the user's questions,
#      respond about the plant's condition or engage in personified interaction.
#      Your tone should be natural, as if the plant itself is speaking.
#      """
#  )
#
# @ChatbotAgent.system_prompt
# def format_user_context(doc_ctx: RunContext[ChatMessage]) -> str:
#     user_msg: ChatMessage = doc_ctx.deps.content
#     """
#     System prompt: Defines the AI’s role, behavior, and tasks for the Agent.
#
#     Args:
#         None
#
#     Returns:
#         str: The system prompt text sent to the LLM, specifying the AI’s identity, tone, and execution logic.
#     """
#     return (
#         f"Plant ID: {user_msg.plant_id}\n"
#         f"User Message: {user_msg.content}\n"
#     )