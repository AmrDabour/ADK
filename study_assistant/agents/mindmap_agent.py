import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

def create_mindmap_agent(name: str = "mindmap_agent") -> Agent:
    return Agent(
        model=LiteLlm(
            model="ollama/gemma4:e2b",
            api_base=os.getenv("OLLAMA_BASE_URL"),
        ),
        name=name,
        description="Builds a text-based mind map from a topic or research content.",
        instruction=(
            "You are a mind map specialist. Given a topic or content, produce a hierarchical text "
            "mind map using indentation to represent depth. Format:\n"
            "[Central Topic]\n"
            "  ├── [Main Branch 1]\n"
            "  │     ├── [Sub-topic 1.1]\n"
            "  │     └── [Sub-topic 1.2]\n"
            "  ├── [Main Branch 2]\n"
            "  ...\n"
            "Include at least 3 main branches with 2-3 sub-topics each."
        ),
    )


mindmap_agent = create_mindmap_agent()
