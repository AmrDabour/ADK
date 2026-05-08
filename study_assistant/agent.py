import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool
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
    description="Orchestrates specialized study agents as tools.",
    instruction=(
        "You are a study assistant orchestrator. Use the available tools to produce the final answer.\n"
        "Tool usage order:\n"
        "1) Call research_agent with the topic.\n"
        "2) Call summary_agent using research output.\n"
        "3) Call quiz_agent using summary or research output.\n"
        "4) Call flashcard_agent using summary or research output.\n"
        "5) Call mindmap_agent using summary or research output.\n"
        "Then return one final response with sections: RESEARCH, SUMMARY, QUIZ, FLASHCARDS, MINDMAP."
    ),
    tools=[
        AgentTool(create_research_agent()),
        AgentTool(create_summary_agent()),
        AgentTool(create_quiz_agent()),
        AgentTool(create_flashcard_agent()),
        AgentTool(create_mindmap_agent()),
    ],
)
