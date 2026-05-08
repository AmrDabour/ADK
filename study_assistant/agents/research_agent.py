import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

def create_research_agent(name: str = "research_agent") -> Agent:
    return Agent(
        model=LiteLlm(
            model="ollama/gemma4:e2b",
            api_base=os.getenv("OLLAMA_BASE_URL"),
        ),
        name=name,
        description="Researches a given topic and returns structured factual content.",
        instruction=(
            "You are a research specialist. When given a topic, provide a thorough, "
            "well-structured overview covering key concepts, important facts, and context. "
            "Output in clear sections: Overview, Key Concepts, Important Details, and Further Reading."
        ),
    )


research_agent = create_research_agent()
