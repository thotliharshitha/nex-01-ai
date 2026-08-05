import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


def ask_question(vector_store, question):

    if not api_key:
        raise ValueError("GOOGLE_API_KEY missing in .env file")


    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=api_key,
        temperature=0.2
    )


    # Retrieve relevant PDF content
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4
        }
    )


    docs = retriever.invoke(question)


    # Combine retrieved chunks
    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )


    # Prompt for RAG
    prompt = f"""
You are NEX-01 AI Study Assistant.

Answer the user's question using only the provided document context.

If the answer is not available in the document, say:
"I could not find this information in the document."

Document Context:
{context}

Question:
{question}

Answer:
"""


    # Gemini response
    response = llm.invoke(prompt)


    # Clean response formatting
    if isinstance(response.content, list):

        for item in response.content:
            if isinstance(item, dict) and "text" in item:
                return item["text"]

        return str(response.content)


    return response.content