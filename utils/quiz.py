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
    raise ValueError(
        "GOOGLE_API_KEY not found!"
    )


# =========================================================
# Gemini model
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0.3,
)


# =========================================================
# Generate Quiz
# =========================================================

def generate_quiz(text):

    # Clean PDF text
    text = text.replace("\n", " ").strip()

    # Limit input size
    text = text[:15000]

    prompt = f"""
You are an expert teacher.

Read the following PDF content and create a quiz.

Rules:

1. Generate exactly 10 MCQ questions.
2. Questions must come ONLY from the PDF.
3. Each question must have exactly 4 options.
4. Only one answer is correct.
5. Give a short explanation.
6. Return ONLY valid JSON.
7. Do not use markdown.
8. Do not add extra text.

JSON FORMAT:

[
  {{
    "question": "Question text",
    "options": [
      "Option 1",
      "Option 2",
      "Option 3",
      "Option 4"
    ],
    "answer": "Correct option text",
    "explanation": "Short explanation"
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
        # LangChain/Gemini may return a list
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
        # Convert JSON text to Python list
        # =================================================

        quiz = json.loads(content)

        # =================================================
        # Validate quiz
        # =================================================

        if not isinstance(quiz, list):

            return []

        valid_questions = []

        for question in quiz:

            if not isinstance(question, dict):
                continue

            if "question" not in question:
                continue

            if "options" not in question:
                continue

            if "answer" not in question:
                continue

            if "explanation" not in question:
                continue

            if not isinstance(
                question["options"],
                list
            ):
                continue

            if len(question["options"]) != 4:
                continue

            valid_questions.append(
                {
                    "question": str(
                        question["question"]
                    ).strip(),

                    "options": [
                        str(option).strip()
                        for option in question["options"]
                    ],

                    "answer": str(
                        question["answer"]
                    ).strip(),

                    "explanation": str(
                        question["explanation"]
                    ).strip()
                }
            )

        # Return maximum 10 questions
        return valid_questions[:10]

    except Exception as e:

        print("Quiz Error:", e)

        return []