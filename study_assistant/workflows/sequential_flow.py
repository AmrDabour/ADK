from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from study_assistant.agents import (
    create_research_agent,
    create_summary_agent,
    create_quiz_agent,
)


async def _run_agent(runner: Runner, session_id: str, user_id: str, message: str) -> str:
    content = types.Content(role="user", parts=[types.Part(text=message)])
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text
    return response_text


async def run_sequential(topic: str) -> dict:
    session_service = InMemorySessionService()
    shared_state = {}

    research_runner = Runner(
        agent=create_research_agent(),
        app_name="study_assistant",
        session_service=session_service,
    )
    research_session = await session_service.create_session(
        app_name="study_assistant", user_id="user", state={}
    )
    research_output = await _run_agent(
        research_runner, research_session.id, "user", f"Research this topic: {topic}"
    )
    shared_state["research"] = research_output

    summary_runner = Runner(
        agent=create_summary_agent(),
        app_name="study_assistant",
        session_service=session_service,
    )
    summary_session = await session_service.create_session(
        app_name="study_assistant", user_id="user", state={}
    )
    summary_output = await _run_agent(
        summary_runner,
        summary_session.id,
        "user",
        f"Summarize the following content:\n\n{research_output}",
    )
    shared_state["summary"] = summary_output

    quiz_runner = Runner(
        agent=create_quiz_agent(),
        app_name="study_assistant",
        session_service=session_service,
    )
    quiz_session = await session_service.create_session(
        app_name="study_assistant", user_id="user", state={}
    )
    quiz_output = await _run_agent(
        quiz_runner,
        quiz_session.id,
        "user",
        f"Create a quiz based on this content:\n\n{research_output}",
    )
    shared_state["quiz"] = quiz_output

    return shared_state
