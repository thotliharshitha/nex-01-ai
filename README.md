# 🚀 NEX-01 AI Study Assistant

<p align="center">
  An AI-powered learning assistant that transforms PDF documents into an interactive study experience using Generative AI and Retrieval-Augmented Generation (RAG).
</p>

---

## 📌 Project Overview

**NEX-01 AI Study Assistant** is an intelligent document-based learning platform designed to help students understand and interact with large academic documents efficiently.

The application allows users to upload PDF documents and communicate with them using Artificial Intelligence. It uses **Retrieval-Augmented Generation (RAG)** architecture combined with **LangChain, FAISS Vector Database, and Google Gemini AI** to provide accurate, context-aware responses.

Instead of manually searching through hundreds of pages, students can instantly ask questions, generate summaries, create quizzes, prepare flashcards, and download study materials.

The main goal of NEX-01 is to create a personalized AI learning companion that improves productivity, revision speed, and knowledge retention.

---

# ✨ Key Features

## 📄 Intelligent PDF Processing

- Upload academic PDF documents.
- Extract text automatically.
- Process large documents efficiently.
- Convert document content into searchable AI knowledge.

---

## 💬 Chat With Your Documents

- Ask questions directly from uploaded PDFs.
- Receive AI-generated answers based on document context.
- Uses RAG pipeline to reduce irrelevant responses.
- Provides interactive document conversations.

---

## 📝 AI Summary Generator

- Generates structured summaries from documents.
- Converts lengthy content into concise study notes.
- Helps students during quick revision.

---

## ❓ Important Questions Generator

- Creates important questions from uploaded materials.
- Helps in exam preparation.
- Identifies key concepts from documents.

---

## 🧠 AI MCQ Quiz Generator

- Generates multiple-choice questions automatically.
- Provides an effective self-assessment method.
- Improves understanding through practice.

---

## 🔖 AI Flashcard Generator

- Creates quick revision flashcards.
- Helps in memorization and active learning.
- Useful for last-minute preparation.

---

## 📥 Download Study Materials

Users can download:

- AI-generated summaries.
- Quiz questions.
- Flashcards.
- Study notes.

---

## 🕒 Chat History

- Maintains previous conversations.
- Improves user experience.
- Allows users to revisit discussions.

---

# 🏗️ System Architecture

```
                 User
                  |
                  ↓
          Streamlit Interface
                  |
                  ↓
            PDF Upload
                  |
                  ↓
        Text Extraction (PyPDF)
                  |
                  ↓
          Text Chunking
                  |
                  ↓
       Gemini Embedding Model
                  |
                  ↓
          FAISS Vector Store
                  |
                  ↓
        Retrieval Augmented Generation
                  |
                  ↓
          Google Gemini AI
                  |
                  ↓
          Intelligent Response
```

---

# 🛠️ Tech Stack

## Programming Language

- Python

## Frontend Framework

- Streamlit

## Artificial Intelligence

- Google Gemini AI
- Generative AI
- Retrieval-Augmented Generation (RAG)

## AI Frameworks

- LangChain
- LangChain Community

## Vector Database

- FAISS (Facebook AI Similarity Search)

## PDF Processing

- PyPDF

## Environment Management

- python-dotenv

## Document Generation

- ReportLab

---

# 📂 Project Structure

```
AI-Study-Assistant/
│
├── app.py
├── Home.py
├── README.md
├── requirements.txt
├── .env
├── .gitignore
│
├── pages/
│   ├── Chat.py
│   ├── Summary.py
│   ├── Quiz.py
│   ├── Flashcards.py
│   └── Notes.py
│
├── utils/
│   ├── pdf_reader.py
│   ├── embeddings.py
│   ├── chatbot.py
│   ├── summary.py
│   ├── quiz.py
│   └── pdf_generator.py
│
├── data/
│   ├── uploads/
│   ├── vector_store/
│   └── chat_history/
│
└── venv/
```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/nex-01-ai.git
```

## 2. Navigate to Project Folder

```bash
cd AI-Study-Assistant
```

## 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Configuration

Create a `.env` file in the project root directory.

Add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

# ▶️ Run Application

Start Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🔄 Working Flow

```
Upload PDF
     ↓
Extract Text
     ↓
Split Into Chunks
     ↓
Generate Embeddings
     ↓
Store in FAISS Database
     ↓
Retrieve Relevant Information
     ↓
Generate AI Response
```

---

# 📸 Screenshots

Screenshots will be added after final UI capture.

## Home Page

(Add Screenshot)

## Chat Page

(Add Screenshot)

## Summary Page

(Add Screenshot)

## Quiz Page

(Add Screenshot)

## Flashcards Page

(Add Screenshot)

---

# 🚀 Future Enhancements

- Multi-PDF conversation support.
- User authentication system.
- Cloud deployment.
- Supabase database integration.
- AI voice assistant.
- Personalized learning dashboard.
- Mobile application.
- Learning analytics.

---

# 🗺️ Development Roadmap

## Completed Features

✅ PDF Upload  
✅ Text Extraction  
✅ Document Chunking  
✅ AI Embeddings  
✅ FAISS Vector Search  
✅ Gemini AI Integration  
✅ Chat With PDF  
✅ AI Summary Generation  
✅ Quiz Generation  
✅ Flashcard Generation  
✅ PDF Downloads  

## Upcoming Features

⬜ Multi-document Chat  
⬜ User Login  
⬜ Cloud Storage  
⬜ Voice AI  
⬜ Analytics Dashboard  

---

# 🎯 Why NEX-01?

NEX-01 combines Artificial Intelligence, Natural Language Processing, and modern Retrieval-Augmented Generation techniques to create a smarter way of learning from documents.

It demonstrates practical implementation of:

- Generative AI
- Large Language Models
- Vector Databases
- RAG Architecture
- AI Application Development

---

# 👩‍💻 Author

**Harshitha Thotli**

B.Tech Computer Science Engineering  
Specialization: Artificial Intelligence & Machine Learning

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.
