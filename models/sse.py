def sse_event(event_type: str, content: Dict[str, Any]) -> str:
    """SSE 格式化：event + JSON data"""
    result = {
        "event": event_type,
        "data": content,
    }
    return json.dumps(result)


async def safe_stream(generator: AsyncGenerator[str, None]):
    """包裝 generator，遇到例外時回傳 error 事件"""
    try:
        async for chunk in generator:
            yield chunk
    except Exception as exc:
        logging.error("SSE stream error", exc_info=True)
        yield sse_event("error", {"message": str(exc)})


def create_event_stream(agent: Agent, prompt, deps):
    """
    Create a common event stream function that can be used by all API endpoints.

    Args:
        agent: The agent to run the prompt against
        prompt: The user prompt
        deps: The dependencies to pass to the agent

    Returns:
        A generator function that yields SSE formatted events
    """

    async def event_stream():
        try:
            async with agent.iter(prompt, deps=deps) as agent_run:
                async for node in agent_run:
                    if Agent.is_user_prompt_node(node):
                        # Format user prompt as a JSON object with a type
                        yield sse_event("user_prompt", {"text": node.user_prompt})

                    elif Agent.is_model_request_node(node):
                        # Indicate assistant is thinking
                        yield sse_event(
                            "thinking", {"text": "Assistant is thinking..."}
                        )

                        async with node.stream(agent_run.ctx) as request_stream:
                            assistant_response = ""

                            async for event in request_stream:
                                # Start of a new part (tool call or text)
                                if isinstance(event, PartStartEvent):
                                    part_info = {
                                        "index": event.index,
                                        "part_type": type(event.part).__name__,
                                    }
                                    if hasattr(event.part, "tool_name"):
                                        part_info["tool_name"] = event.part.tool_name

                                    yield sse_event("part_start", part_info)

                                elif isinstance(event, PartDeltaEvent):
                                    # Regular text response
                                    if isinstance(event.delta, TextPartDelta):
                                        assistant_response += event.delta.content_delta
                                        yield sse_event(
                                            "text_delta",
                                            {
                                                "text": event.delta.content_delta,
                                                "full_text": assistant_response,
                                            },
                                        )

                                    elif isinstance(event.delta, ToolCallPartDelta):
                                        # Tool call parameters
                                        yield sse_event(
                                            "tool_call_delta",
                                            {"args": event.delta.args_delta},
                                        )

                                elif isinstance(event, FinalResultEvent):
                                    # End of model generation
                                    yield sse_event(
                                        "final_result",
                                        {
                                            "tool_name": (
                                                event.tool_name
                                                if event.tool_name
                                                else "None"
                                            )
                                        },
                                    )

                    elif Agent.is_call_tools_node(node):
                        async with node.stream(agent_run.ctx) as handle_stream:
                            async for event in handle_stream:
                                if isinstance(event, FunctionToolCallEvent):
                                    # Tool being called
                                    yield sse_event(
                                        "tool_call",
                                        {
                                            "tool_name": event.part.tool_name,
                                            "args": event.part.args,
                                        },
                                    )

                                elif isinstance(event, FunctionToolResultEvent):
                                    # Result from tool call
                                    try:
                                        result = event.result.content.dict()
                                    except Exception as e:
                                        result = str(event.result.content)
                                    yield sse_event("tool_result", {"result": result})

                    # Send complete response at the end
                    elif Agent.is_end_node(node):
                        if hasattr(agent_run, "result") and hasattr(
                            agent_run.result, "output"
                        ):
                            if not isinstance(agent_run.result.output, str):
                                yield sse_event(
                                    "final_answer",
                                    {"text": agent_run.result.output.dict()},
                                )

        except Exception as e:
            # Log the full error details
            logging.error(f"Error in event stream: {e}")
            logging.error(traceback.format_exc())
            print(f"Error occurred: {e}")
            print(traceback.format_exc())
            yield sse_event("error", {"message": str(e)})

    return event_stream

