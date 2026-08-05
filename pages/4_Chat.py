import streamlit as st

from utils.chatbot import ask_question
from utils.pdf_generator import create_chat_pdf


st.set_page_config(
    page_title="NEX-01 AI Chat",
    layout="wide"
)


st.title("NEX-01 AI Chat")


# Check PDF availability
if "vector_store" not in st.session_state:

    st.warning(
        "Please upload a PDF first."
    )

    st.stop()


st.success(
    "Document ready. Ask questions from your PDF."
)


# Chat history initialize
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# Download Chat PDF
if st.session_state.chat_history:

    pdf = create_chat_pdf(
        st.session_state.chat_history
    )

    st.download_button(
        label="Download Chat PDF",
        data=pdf,
        file_name="NEX-01_AI_Chat.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.divider()


# Display previous chats
for chat in st.session_state.chat_history:

    if chat["role"] == "user":

        with st.container(border=True):

            st.markdown("**You**")

            st.write(chat["message"])

    else:

        with st.container(border=True):

            st.markdown("**NEX-01 AI**")

            st.write(chat["message"])


# User input
question = st.chat_input(
    "Ask something from your PDF..."
)


if question:

    # Save user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "message": question
        }
    )

    with st.spinner("Thinking..."):

        answer = ask_question(
            st.session_state.vector_store,
            question
        )

    # Save AI response
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "message": answer
        }
    )

    st.rerun()