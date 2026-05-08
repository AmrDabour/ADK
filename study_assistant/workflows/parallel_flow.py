import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from study_assistant.agents import (
    create_flashcard_agent,
    create_mindmap_agent,
    create_quiz_agent,
)


async def _run_agent(runner: Runner, session_service: InMemorySessionService, user_id: str, message: str) -> str:
    session = await session_service.create_session(
        app_name="study_assistant", user_id=user_id, state={}
    )
    content = types.Content(role="user", parts=[types.Part(text=message)])
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text
    return response_text


async def run_parallel(topic: str, research_content: str) -> dict:
    session_service = InMemorySessionService()

    flashcard_runner = Runner(
        agent=create_flashcard_agent(),
        app_name="study_assistant",
        session_service=session_service,
    )
    mindmap_runner = Runner(
        agent=create_mindmap_agent(),
        app_name="study_assistant",
        session_service=session_service,
    )
    quiz_runner = Runner(
        agent=create_quiz_agent(),
        app_name="study_assistant",
        session_service=session_service,
    )

    flashcard_task = _run_agent(
        flashcard_runner,
        session_service,
        "user",
        f"Create flashcards for this content:\n\n{research_content}",
    )
    mindmap_task = _run_agent(
        mindmap_runner,
        session_service,
        "user",
        f"Build a mind map for the topic: {topic}\n\nContent:\n{research_content}",
    )
    quiz_task = _run_agent(
        quiz_runner,
        session_service,
        "user",
        f"Generate a quiz from this content:\n\n{research_content}",
    )

    flashcards, mindmap, quiz = await asyncio.gather(
        flashcard_task, mindmap_task, quiz_task
    )

    return {
        "flashcards": flashcards,
        "mindmap": mindmap,
        "quiz": quiz,
    }
