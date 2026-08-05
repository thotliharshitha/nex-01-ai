import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found! Check your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

# Load Gemini Model
model = genai.GenerativeModel("gemini-flash-latest")


def generate_summary(text):

    # Clean extracted text
    text = text.replace("\n", " ").strip()

    # Limit input size
    text = text[:3000]

    prompt = f"""
You are NEX-01 AI Study Assistant.

Your task is to analyze the uploaded study material and generate a professional academic summary for university students.

Instructions:

- Read the study material carefully.
- Extract only the most important information.
- Use clear, simple, and professional English.
- Do NOT copy long paragraphs directly from the document.
- Organize the output with proper headings.
- Use bullet points wherever appropriate.
- Keep explanations concise and exam-oriented.
- Include only information present in the uploaded document.
- Do NOT repeat instructions in the output.
- Do NOT write phrases like:
  - Concept Name
  - Brief explanation in 1–2 sentences

--------------------------------------------------

# IMPORTANT POINTS

- List the most important points.
- Keep each point short.
- Focus on exam preparation.

--------------------------------------------------

# KEY CONCEPTS

Extract the 5–10 most important concepts.

For every concept use this format:

### Concept Name

Explanation in 1–2 simple sentences.

Example:

### Cloud Computing

Cloud computing provides on-demand access to shared computing resources over the Internet.

### Virtualization

Virtualization allows multiple virtual machines to run on a single physical computer.

Rules:

- Do NOT write "Concept Name:"
- Do NOT write "Brief explanation:"
- Do NOT number the concepts.
- Keep explanations concise.

--------------------------------------------------

# SHORT EXAM NOTES

Include:

- Important definitions
- Important keywords
- Important formulas (if available)
- Important characteristics
- Advantages
- Disadvantages
- Comparisons
- Frequently asked concepts

--------------------------------------------------

# SUMMARY

Write a short conclusion (4–6 sentences) summarizing the overall topic.

--------------------------------------------------

Study Material:

{text}
"""

    try:

        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "No summary could be generated."

    except Exception as e:
        return f"Error generating summary: {str(e)}"