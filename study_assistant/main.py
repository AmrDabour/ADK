import asyncio

from study_assistant.workflows.sequential_flow import run_sequential
from study_assistant.workflows.parallel_flow import run_parallel


def print_section(title: str, content: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    print(content)


async def main():
    topic = input("Enter a study topic: ").strip()
    if not topic:
        topic = "Photosynthesis"

    workflow = input("Choose workflow (1=sequential, 2=parallel): ").strip().lower()
    if workflow in {"1", "sequential", "s"}:
        print(f"\nStarting sequential workflow for: {topic}")
        sequential_results = await run_sequential(topic)
        print_section("RESEARCH", sequential_results.get("research", ""))
        print_section("SUMMARY", sequential_results.get("summary", ""))
        print_section("QUIZ (Sequential)", sequential_results.get("quiz", ""))
        return

    if workflow in {"2", "parallel", "p"}:
        print(f"\nStarting parallel workflow for: {topic}")
        parallel_results = await run_parallel(
            topic=topic,
            research_content=topic,
        )
        print_section("FLASHCARDS", parallel_results.get("flashcards", ""))
        print_section("MIND MAP", parallel_results.get("mindmap", ""))
        print_section("QUIZ (Parallel)", parallel_results.get("quiz", ""))
        return

    print("Invalid workflow choice")


if __name__ == "__main__":
    asyncio.run(main())
