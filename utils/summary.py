import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# Load .env file
# =========================================================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# =========================================================
# Get API key
# =========================================================

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please check your .env file."
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
# Generate Summary
# =========================================================

def generate_summary(text):
    """
    Generate a concise summary from the uploaded PDF text.
    """

    if not text or not text.strip():
        return "No text was extracted from the PDF."

    prompt = f"""
You are NEX-01 AI Study Assistant.

Create a clear and concise summary of the following study material.

Requirements:

- Include the main concepts.
- Include important definitions.
- Include important key points.
- Use simple and easy-to-understand language.
- Organize the summary using headings and bullet points.
- Do not add information that is not present in the study material.
- Return ONLY the summary.
- Do not return JSON.
- Do not return a Python list.
- Do not return a dictionary.

Study Material:

{text}
"""

    try:

        # Send request to Gemini
        response = llm.invoke(prompt)

        content = response.content

        # =================================================
        # Gemini may return content as a list
        # =================================================

        if isinstance(content, list):

            extracted_text = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":

                        extracted_text.append(
                            item.get("text", "")
                        )

                elif isinstance(item, str):

                    extracted_text.append(item)

            content = "\n".join(extracted_text)

        # =================================================
        # Make sure content is a string
        # =================================================

        if not isinstance(content, str):
            content = str(content)

        content = content.strip()

        # =================================================
        # Check empty response
        # =================================================

        if not content:
            return "Unable to generate the summary."

        return content

    except Exception as e:

        return f"Summary generation failed: {str(e)}"