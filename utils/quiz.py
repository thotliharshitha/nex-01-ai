import os
import json
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found!")


# Gemini configuration
genai.configure(api_key=api_key)


model = genai.GenerativeModel(
    "gemini-flash-latest"
)


def generate_quiz(text):

    # Clean PDF text
    text = text.replace("\n", " ").strip()

    # Limit tokens
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
  "question":"Question text",
  "options":[
    "Option 1",
    "Option 2",
    "Option 3",
    "Option 4"
  ],
  "answer":"Correct option text",
  "explanation":"Short explanation"
 }}
]


PDF CONTENT:

{text}

"""


    try:

        response = model.generate_content(prompt)


        content = response.text.strip()


        # Remove markdown if Gemini adds it

        if content.startswith("```json"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )


        elif content.startswith("```"):

            content = content.replace(
                "```",
                ""
            )


        quiz = json.loads(content)


        return quiz


    except Exception as e:

        print("Quiz Error:",e)

        return []