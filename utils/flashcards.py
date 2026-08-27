import os
import json
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# Load .env
# =========================================================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# =========================================================
# Get API key
# =========================================================

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found!")


# =========================================================
# Gemini model
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0.3,
)


# =========================================================
# Generate Flashcards
# =========================================================

def generate_flashcards(text):

    # Clean PDF text
    text = text.replace("\n", " ").strip()

    # Limit PDF content
    text = text[:15000]

    prompt = f"""
You are an expert teacher.

Create flashcards from the PDF content.

Rules:

1. Generate exactly 10 flashcards.
2. Questions must be based ONLY on the PDF.
3. Answers should be short and easy to understand.
4. Return ONLY valid JSON.
5. Do not add markdown.
6. Do not add any explanation outside the JSON.

JSON FORMAT:

[
  {{
    "question": "Question here",
    "answer": "Answer here"
  }}
]

PDF CONTENT:

{text}
"""

    try:

        # Send request to Gemini
        response = llm.invoke(prompt)

        content = response.content

        # =================================================
        # Gemini/LangChain may return a list
        # =================================================

        if isinstance(content, list):

            parts = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":

                        parts.append(
                            item.get("text", "")
                        )

                elif isinstance(item, str):

                    parts.append(item)

            content = "\n".join(parts)

        # Make sure content is a string
        content = str(content).strip()

        # =================================================
        # Remove markdown code fences
        # =================================================

        if content.startswith("```json"):

            content = content[7:]

        elif content.startswith("```"):

            content = content[3:]

        if content.endswith("```"):

            content = content[:-3]

        content = content.strip()

        # =================================================
        # Convert JSON to Python
        # =================================================

        flashcards = json.loads(content)

        # =================================================
        # Validate response
        # =================================================

        if not isinstance(flashcards, list):

            return []

        valid_flashcards = []

        for card in flashcards:

            if not isinstance(card, dict):
                continue

            if "question" not in card:
                continue

            if "answer" not in card:
                continue

            question = str(
                card["question"]
            ).strip()

            answer = str(
                card["answer"]
            ).strip()

            if not question or not answer:
                continue

            valid_flashcards.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        # Return maximum 10 flashcards
        return valid_flashcards[:10]

    except Exception as e:

        print("Flashcard Error:", e)

        return []