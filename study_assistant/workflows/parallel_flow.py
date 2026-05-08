import asyncio
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from study_assistant.agents import (
    create_flashcard_agent,
    create_mindmap_agent,
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


async def run_parallel(topic: str, research_content: str) -> dict[str, str]:
    session_service = InMemorySessionService()

    flashcard_task = _ask(
        create_flashcard_agent(),
        f"Create flashcards for this content:\n\n{research_content}",
        session_service,
    )
    mindmap_task = _ask(
        create_mindmap_agent(),
        f"Build a mind map for the topic: {topic}\n\nContent:\n{research_content}",
        session_service,
    )
    quiz_task = _ask(
        create_quiz_agent(),
        f"Generate a quiz from this content:\n\n{research_content}",
        session_service,
    )

    flashcards, mindmap, quiz = await asyncio.gather(
        flashcard_task, mindmap_task, quiz_task
    )

    return {
        "flashcards": flashcards,
        "mindmap": mindmap,
        "quiz": quiz,
    }
