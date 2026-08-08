import streamlit as st

from utils.pdf_reader import extract_text
from utils.embeddings import create_vector_store
from utils.chatbot import ask_question
from utils.pdf_generator import create_chat_pdf


st.set_page_config(
    page_title="NEX-01 AI Chat",
    layout="wide"
)


st.title("NEX-01 AI Chat")

st.caption(
    "Ask questions from your uploaded PDF."
)

st.divider()


# =========================================================
# PDF UPLOAD
# =========================================================

st.subheader("Upload Your Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        "PDF uploaded successfully."
    )

    with st.spinner("Reading document..."):

        text = extract_text(
            uploaded_file
        )

    if not text.strip():

        st.error(
            "Could not extract text from the PDF."
        )

        st.stop()


    with st.spinner(
        "Preparing document for chat..."
    ):

        vector_store = create_vector_store(
            text
        )

    st.session_state[
        "vector_store"
    ] = vector_store

    st.success(
        "Document ready. You can now ask questions."
    )


# =========================================================
# CHECK VECTOR STORE
# =========================================================

if "vector_store" not in st.session_state:

    st.info(
        "Upload a PDF above to start chatting."
    )

    st.stop()


st.divider()


# =========================================================
# CHAT HISTORY
# =========================================================

if "chat_history" not in st.session_state:

    st.session_state[
        "chat_history"
    ] = []


# =========================================================
# DISPLAY CHAT
# =========================================================

st.subheader("Chat")


for chat in st.session_state[
    "chat_history"
]:

    if chat["role"] == "user":

        with st.container(border=True):

            st.markdown(
                "**You**"
            )

            st.write(
                chat["message"]
            )


    elif chat["role"] == "assistant":

        with st.container(border=True):

            st.markdown(
                "**NEX-01 AI**"
            )

            st.write(
                chat["message"]
            )


# =========================================================
# ASK QUESTION
# =========================================================

question = st.chat_input(
    "Ask something from your PDF..."
)


if question:

    st.session_state[
        "chat_history"
    ].append(
        {
            "role": "user",
            "message": question
        }
    )


    with st.spinner(
        "Thinking..."
    ):

        answer = ask_question(
            st.session_state[
                "vector_store"
            ],
            question
        )


    st.session_state[
        "chat_history"
    ].append(
        {
            "role": "assistant",
            "message": answer
        }
    )


    st.rerun()


# =========================================================
# DOWNLOAD CHAT PDF
# =========================================================

if st.session_state[
    "chat_history"
]:

    st.divider()

    st.subheader(
        "Download Chat"
    )

    pdf = create_chat_pdf(
        st.session_state[
            "chat_history"
        ]
    )


    st.download_button(
        label="Download Chat PDF",
        data=pdf,
        file_name="NEX-01_AI_Chat.pdf",
        mime="application/pdf",
        use_container_width=True
    )