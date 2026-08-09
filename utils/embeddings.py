from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


# =========================================================
# HUGGING FACE EMBEDDINGS
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# SPLIT TEXT
# =========================================================

def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    return chunks


# =========================================================
# CREATE FAISS VECTOR STORE
# =========================================================

def create_vector_store(text):

    if not text or not text.strip():
        raise ValueError(
            "No text was found in the document."
        )

    chunks = split_text(text)

    if not chunks:
        raise ValueError(
            "Could not create text chunks from the document."
        )

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vector_store