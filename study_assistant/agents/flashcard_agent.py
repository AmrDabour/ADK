import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

def create_flashcard_agent(name: str = "flashcard_agent") -> Agent:
    return Agent(
        model=LiteLlm(
            model="ollama/gemma4:e2b",
            api_base=os.getenv("OLLAMA_BASE_URL"),
        ),
        name=name,
        description="Creates flashcards from study material for active recall practice.",
        instruction=(
            "You are a flashcard creator. Given study material or a topic, generate 8 flashcards. "
            "Each flashcard must follow this exact format:\n"
            "FRONT: <term or question>\n"
            "BACK: <definition or answer>\n"
            "---\n"
            "Make the fronts concise and the backs informative but brief."
        ),
    )


flashcard_agent = create_flashcard_agent()
