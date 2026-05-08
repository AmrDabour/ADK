import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

def create_quiz_agent(name: str = "quiz_agent") -> Agent:
    return Agent(
        model=LiteLlm(
            model="ollama/gemma4:e2b",
            api_base=os.getenv("OLLAMA_BASE_URL"),
        ),
        name=name,
        description="Generates quiz questions from study material.",
        instruction=(
            "You are a quiz creator. Given study material or a topic, generate 5 multiple-choice "
            "questions with 4 options each (A, B, C, D). Clearly mark the correct answer for each "
            "question at the end. Format each question as:\n"
            "Q#: <question>\n"
            "A) ...\nB) ...\nC) ...\nD) ...\n"
            "Answer: <letter>"
        ),
    )


quiz_agent = create_quiz_agent()
