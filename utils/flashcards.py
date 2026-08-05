import os
import json
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


# Load .env file

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)


api_key = os.getenv("GOOGLE_API_KEY")


if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")


genai.configure(
    api_key=api_key
)


model = genai.GenerativeModel(
    "gemini-flash-latest"
)



def generate_flashcards(text):

    text = text.replace("\n", " ").strip()

    # Limit PDF content
    text = text[:15000]


    prompt = f"""

You are an expert teacher.

Create flashcards from the PDF content.

Rules:

1. Generate exactly 10 flashcards.
2. Questions must be based only on the PDF.
3. Answers should be short and easy to understand.
4. Return only JSON.
5. Do not add markdown.


JSON FORMAT:

[
 {{
   "question":"Question here",
   "answer":"Answer here"
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

            content = content.replace("```json", "")
            content = content.replace("```", "")


        elif content.startswith("```"):

            content = content.replace("```", "")



        flashcards = json.loads(content)


        return flashcards



    except Exception as e:

        print("Flashcard Error:", e)

        return []