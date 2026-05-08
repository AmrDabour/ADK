import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

def create_summary_agent(name: str = "summary_agent") -> Agent:
    return Agent(
        model=LiteLlm(
            model="ollama/gemma4:e2b",
            api_base=os.getenv("OLLAMA_BASE_URL"),
        ),
        name=name,
        description="Summarizes content into concise, easy-to-review notes.",
        instruction=(
            "You are a summarization expert. Given content, produce a concise summary that captures "
            "the most important points. Structure the output as:\n"
            "- TL;DR (1-2 sentences)\n"
            "- Key Takeaways (bullet list)\n"
            "- Conclusion"
        ),
    )


summary_agent = create_summary_agent()
