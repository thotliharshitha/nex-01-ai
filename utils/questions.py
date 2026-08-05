from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate


def generate_questions(text):

    llm = OllamaLLM(
        model="llama3.2",
        temperature=0.5
    )

    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
You are an AI Study Assistant.

Generate 5 important exam questions from the given study material.

Include:
- Question
- Answer

Keep answers short and easy to understand.

Study Material:
{text}
"""
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "text": text[:6000]
        }
    )

    return response