import os
import streamlit as st
from pypdf import PdfReader

from utils.embeddings import create_vector_store


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="NEX-01 AI Study Assistant",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("NEX-01")
st.subheader("AI Study Assistant")

st.caption("AI-powered PDF Learning Platform")

st.divider()

# --------------------------------------------------
# Upload Section
# --------------------------------------------------

st.subheader("Upload Your Study Material")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

# --------------------------------------------------
# Process PDF
# --------------------------------------------------

if uploaded_file is not None:

    with st.spinner("Processing document..."):

        reader = PdfReader(uploaded_file)

        extracted_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                extracted_text += text

        # Save extracted text
        st.session_state["pdf_text"] = extracted_text

        # Create vector store
        vector_store = create_vector_store(
            extracted_text
        )

        st.session_state["vector_store"] = vector_store

        # Save extracted text locally
        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            "data/extracted_text.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(extracted_text)

    st.success(
        "Document processed successfully."
    )

else:

    st.info(
        "Upload your study material to get started."
    )

st.divider()

st.caption(
    "Version 1.0 | NEX-01 AI Study Assistant"
)