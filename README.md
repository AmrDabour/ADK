# Study Assistant (ADK)

A study assistant application built using the [Google Agent Development Kit (ADK)](https://github.com/google/google-adk). It helps students and learners quickly produce comprehensive study materials (research notes, summaries, quizzes, flashcards, and mind maps) based on any given topic.

## Features

This application orchestrates multiple specialized agents using Ollama and the `gemma4:e2b` model:

- **Research Agent**: Gathers core information and context about the topic.
- **Summary Agent**: Condenses the research into a digestible summary.
- **Quiz Agent**: Generates multiple-choice and short-answer questions to test knowledge.
- **Flashcard Agent**: Creates quick Q&A pairs for spaced repetition.
- **Mind Map Agent**: Produces structured topics/subtopics to visualize the topic.

## Workflows

The assistant offers two main workflows to generate your study layout:

1. **Sequential Workflow**
   Runs agents in a linear order, typically:
   `topic -> Research -> Summary -> Quiz`.
   Output is focused heavily on building a solid foundational understanding first.

2. **Parallel Workflow**
   Runs non-dependent agents simultaneously to generate auxiliary study materials faster.
   Produces **Flashcards**, **Mind Maps**, and a **Quiz** concurrently.

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) running locally (or remotely) with the `gemma4:e2b` model pulled.
- Relevant Google ADK dependencies.

## Installation

1. Clone or navigate into this workspace.
2. Install the necessary Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have the `google-adk` installed)*
   
3. Ensure Ollama is running and has the expected model:
   ```bash
   ollama run gemma4:e2b
   ```

## Usage

You can optionally configure the Ollama endpoint if running it remotely:

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
```

To run the study assistant interactive CLI:

```bash
python -m study_assistant.main
```

1. You will be prompted to enter a study topic (e.g., "Photosynthesis").
2. Then, choose your preferred workflow (1 for Sequential, 2 for Parallel).
3. The agents will process the request and print out the corresponding sections based on your workflow choice.

## Project Structure

- `study_assistant/main.py`: Entry point for the CLI assistant and workflow selection.
- `study_assistant/agent.py`: ADK Agent orchestrator configuration.
- `study_assistant/agents/`: Directory containing individual specialized agents.
- `study_assistant/workflows/`: Implementations of parallel and sequential execution flows.
