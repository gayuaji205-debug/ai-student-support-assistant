"""Command-line AI Student Support Assistant.

This project uses lightweight keyword-based information retrieval so it can
run locally without an API key. It can also send image-based notices through
Tesseract OCR when the optional dependencies are installed.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from ocr_module import extract_text_from_image


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "student_data.txt"
STOP_WORDS = {
    "a",
    "about",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "how",
    "i",
    "is",
    "me",
    "of",
    "on",
    "please",
    "tell",
    "the",
    "to",
    "what",
    "where",
    "when",
    "which",
    "who",
}


def load_documents(path: Path = DATA_FILE) -> Dict[str, str]:
    """Load named knowledge-base sections from a plain-text file."""
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^\[([^\]]+)\]\s*$", text)
    documents: Dict[str, str] = {}

    # The split result is: preamble, heading, content, heading, content...
    for index in range(1, len(sections), 2):
        title = sections[index].strip().replace("_", " ").title()
        content = sections[index + 1].strip()
        if content:
            documents[title] = content

    return documents


def tokenize(text: str) -> List[str]:
    """Return useful lowercase words for matching a student query."""
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [word for word in words if word not in STOP_WORDS and len(word) > 1]


def search_documents(
    query: str, documents: Dict[str, str]
) -> List[Tuple[int, str, str]]:
    """Rank documents by the number of query terms they contain."""
    query_terms = set(tokenize(query))
    ranked: List[Tuple[int, str, str]] = []

    for title, content in documents.items():
        searchable_text = f"{title} {content}".lower()
        score = sum(searchable_text.count(term) for term in query_terms)

        # Give a small boost when the complete query appears in a section.
        if query.strip().lower() in searchable_text:
            score += 3

        if score:
            ranked.append((score, title, content))

    return sorted(ranked, key=lambda item: (-item[0], item[1]))


def answer_query(query: str, documents: Dict[str, str]) -> str:
    """Generate a response from the local student-support knowledge base."""
    matches = search_documents(query, documents)
    if not matches:
        return (
            "I could not find that information in the current resources. "
            "Try asking about exams, guidelines, library, fees, attendance, "
            "or contact details."
        )

    best_score, title, content = matches[0]
    related = [
        related_title
        for score, related_title, _ in matches[1:3]
        if score >= max(1, best_score // 2)
    ]
    response = f"Source: {title}\n{content}"
    if related:
        response += f"\n\nRelated resources: {', '.join(related)}"
    return response


def print_help() -> None:
    """Display commands supported by the terminal assistant."""
    print(
        "\nCommands:\n"
        "  help                 Show this help message\n"
        "  ocr <image-path>     Extract text from a scanned notice\n"
        "  reload               Reload student_data.txt\n"
        "  exit                 Close the assistant\n"
    )


def run_cli() -> None:
    """Run the interactive terminal application."""
    try:
        documents = load_documents()
    except FileNotFoundError:
        print(f"Knowledge base not found: {DATA_FILE}")
        return

    print("=" * 62)
    print("AI STUDENT SUPPORT ASSISTANT")
    print("Ask a question about student resources.")
    print("Type 'help' for commands or 'exit' to quit.")
    print("=" * 62)

    while True:
        try:
            query = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAssistant: Goodbye!")
            break

        if not query:
            continue

        command = query.lower()
        if command in {"exit", "quit", "bye"}:
            print("Assistant: Goodbye!")
            break
        if command == "help":
            print_help()
            continue
        if command == "reload":
            documents = load_documents()
            print(f"Assistant: Reloaded {len(documents)} resources.")
            continue
        if command.startswith("ocr "):
            image_path = query[4:].strip()
            print(f"Assistant: Processing OCR for {image_path}...")
            print(extract_text_from_image(image_path))
            continue

        print(f"\nAssistant:\n{answer_query(query, documents)}")


if __name__ == "__main__":
    run_cli()