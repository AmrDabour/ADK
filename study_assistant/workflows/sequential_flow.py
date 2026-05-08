from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from study_assistant.agents import (
    create_research_agent,
    create_summary_agent,
    create_quiz_agent,
)

APP_NAME = "study_assistant"
USER_ID = "user"


async def _ask(agent: Agent, prompt: str, session_service: InMemorySessionService) -> str:
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state={},
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
    return text


async def run_sequential(topic: str) -> dict[str, str]:
    session_service = InMemorySessionService()
    research = await _ask(
        create_research_agent(),
        f"Research this topic: {topic}",
        session_service,
    )
    summary = await _ask(
        create_summary_agent(),
        f"Summarize the following content:\n\n{research}",
        session_service,
    )
    quiz = await _ask(
        create_quiz_agent(),
        f"Create a quiz based on this content:\n\n{research}",
        session_service,
    )
    return {
        "research": research,
        "summary": summary,
        "quiz": quiz,
    }
