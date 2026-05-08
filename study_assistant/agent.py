import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from study_assistant.agents import (
    create_research_agent,
    create_summary_agent,
    create_quiz_agent,
    create_flashcard_agent,
    create_mindmap_agent,
)


def _model() -> LiteLlm:
    return LiteLlm(
        model="ollama/gemma4:e2b",
        api_base=os.getenv("OLLAMA_BASE_URL"),
    )


root_agent = Agent(
    model=_model(),
    name="study_assistant",
    description="Orchestrates all study agents to help users learn any topic.",
    instruction=(
        "You are the Study Assistant coordinator. You help users learn topics by delegating to "
        "specialized sub-agents:\n"
        "- sa_research_agent: gathers factual content on a topic\n"
        "- sa_summary_agent: condenses content into key points\n"
        "- sa_quiz_agent: creates multiple-choice quiz questions\n"
        "- sa_flashcard_agent: builds flashcards for active recall\n"
        "- sa_mindmap_agent: generates a hierarchical mind map\n\n"
        "When a user provides a topic, coordinate these agents to build a complete study package. "
        "Present results clearly labeled by type."
    ),
    sub_agents=[
        create_research_agent("sa_research_agent"),
        create_summary_agent("sa_summary_agent"),
        create_quiz_agent("sa_quiz_agent"),
        create_flashcard_agent("sa_flashcard_agent"),
        create_mindmap_agent("sa_mindmap_agent"),
    ],
)
