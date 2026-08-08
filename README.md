# NEX-01 AI Study Assistant

An AI-powered Study Assistant using RAG, LangChain, FAISS, and Google Gemini for intelligent document-based learning.

## Overview

NEX-01 AI Study Assistant is an AI-powered learning platform that helps users understand and interact with PDF documents efficiently.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-aware responses using Google Gemini.

Users can upload study material and use AI-powered features for learning, revision, and exam preparation.

## Key Features

### PDF Processing
- Upload PDF documents.
- Extract text from documents.
- Split documents into manageable text chunks.
- Generate embeddings for document content.

### Chat with PDF
- Ask questions about uploaded documents.
- Retrieve relevant document content using FAISS.
- Generate context-aware responses using Google Gemini.
- Maintain chat history during the session.

### AI Summary
- Generate structured summaries from PDF content.
- Convert lengthy documents into concise study material.
- Support faster revision.

### Important Questions
- Generate important questions from study material.
- Identify key concepts from documents.
- Support exam preparation.

### MCQ Quiz
- Generate multiple-choice questions from uploaded content.
- Provide an interactive way to test understanding.
- Support self-assessment and revision.

### AI Flashcards
- Generate concise flashcards from document content.
- Support active recall and memorization.
- Provide quick revision material.

### Study Material Downloads
- Download generated summaries.
- Download quiz content.
- Download flashcards.
- Download generated study material as PDF files.

## System Architecture

```text
User
  |
  v
Streamlit Interface
  |
  v
PDF Upload
  |
  v
Text Extraction
  |
  v
Text Chunking
  |
  v
Embeddings
  |
  v
FAISS Vector Store
  |
  v
Relevant Context Retrieval
  |
  v
Retrieval-Augmented Generation
  |
  v
Google Gemini
  |
  v
AI-Generated Response
```

## Tech Stack

### Programming Language
- Python

### Application Framework
- Streamlit

### Generative AI
- Google Gemini
- Retrieval-Augmented Generation (RAG)

### AI Frameworks
- LangChain
- LangChain Community

### Vector Search
- FAISS

### Document Processing
- PyPDF

### Environment Management
- python-dotenv

### PDF Generation
- ReportLab

## Project Structure

```text
nex-01-ai/
│
├── .streamlit/
│
├── assets/
│   └── screenshots/
│       ├── chat.png
│       ├── flashcards_output.png
│       ├── home.png
│       ├── quiz_output.png
│       ├── summary_input.png
│       ├── summary_output.png
│       └── upload.png
│
├── pages/
│   ├── 1_Summary.py
│   ├── 2_Quiz.py
│   ├── 3_Flashcards.py
│   └── 4_Chat.py
│
├── utils/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── embeddings.py
│   ├── pdf_generator.py
│   ├── pdf_reader.py
│   ├── quiz.py
│   └── summary.py
│
├── .gitignore
├── Home.py
├── README.md
└── requirements.txt
```

Sensitive files such as `.env` and the local virtual environment are excluded from version control.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thotliharshitha/nex-01-ai.git
```

### 2. Navigate to the Project Directory

```bash
cd nex-01-ai
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Configuration

Create a `.env` file in the project root directory.

Add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

Do not commit the `.env` file or expose your API key publicly.

## Run the Application

Start the Streamlit application:

```bash
streamlit run Home.py
```

The application will open in your default web browser.

## Working Flow

```text
Upload PDF
    |
    v
Extract Text
    |
    v
Split Text into Chunks
    |
    v
Generate Embeddings
    |
    v
Store Embeddings in FAISS
    |
    v
Retrieve Relevant Information
    |
    v
Pass Context to Google Gemini
    |
    v
Generate AI Response
```

## Screenshots

### Home Page

![Home Page](assets/screenshots/home.png)

### PDF Upload

![PDF Upload](assets/screenshots/upload.png)

### Chat with PDF

![Chat with PDF](assets/screenshots/chat.png)

### AI Summary

![Summary Input](assets/screenshots/summary_input.png)

![Summary Output](assets/screenshots/summary_output.png)

### MCQ Quiz

![Quiz Output](assets/screenshots/quiz_output.png)

### AI Flashcards

![Flashcards Output](assets/screenshots/flashcards_output.png)

## Development Roadmap

### Completed

- PDF Upload
- PDF Text Extraction
- Text Chunking
- Document Embeddings
- FAISS Vector Search
- Google Gemini Integration
- Retrieval-Augmented Generation
- Chat with PDF
- AI Summary Generation
- Important Questions Generation
- MCQ Quiz Generation
- Flashcard Generation
- Study Material Downloads
- Chat History

### Planned

- Multi-PDF Chat
- User Authentication
- Cloud Storage
- Supabase Integration
- Voice AI
- Personalized Learning Dashboard
- Learning Analytics

## Future Enhancements

The project can be extended with multi-document conversations, user authentication, cloud storage, voice-based interaction, personalized learning dashboards, and learning analytics.

## Why NEX-01?

NEX-01 demonstrates the practical application of Generative AI and Retrieval-Augmented Generation to solve a real-world learning problem.

The project combines:

- Large Language Models
- Retrieval-Augmented Generation
- Vector Search
- Semantic Retrieval
- Document Processing
- Generative AI
- AI Application Development

## Author

**Harshitha Thotli**

B.Tech Computer Science Engineering  
Specialization: Artificial Intelligence & Machine Learning




