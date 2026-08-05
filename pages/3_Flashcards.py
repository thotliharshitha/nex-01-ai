import streamlit as st

from utils.pdf_reader import extract_text
from utils.flashcards import generate_flashcards
from utils.pdf_generator import create_flashcard_pdf


st.set_page_config(
    page_title="AI Flashcards",
    layout="wide"
)


st.title("NEX-01 AI Flashcards")

st.caption(
    "Generate AI-powered flashcards from your uploaded PDF for effective learning."
)


# -------------------------
# Session State
# -------------------------

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []


if "card_index" not in st.session_state:
    st.session_state.card_index = 0


if "show_answer" not in st.session_state:
    st.session_state.show_answer = False



# -------------------------
# Upload PDF
# -------------------------

st.subheader("Upload Study Material")


uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file:

    st.success("PDF uploaded successfully")


    if st.button(
        "Generate Flashcards",
        use_container_width=True
    ):

        with st.spinner(
            "Creating flashcards using AI..."
        ):

            text = extract_text(
                uploaded_file
            )


            cards = generate_flashcards(
                text
            )


            st.session_state.flashcards = cards

            st.session_state.card_index = 0

            st.session_state.show_answer = False



# -------------------------
# Display Flashcards
# -------------------------

if st.session_state.flashcards:


    cards = st.session_state.flashcards

    total = len(cards)

    index = st.session_state.card_index

    card = cards[index]


    st.divider()


    st.subheader("Generated Flashcards")


    st.progress(
        (index + 1) / total
    )


    st.caption(
        f"Card {index + 1} of {total}"
    )


    # Flashcard Container

    with st.container(border=True):


        st.markdown(
            "### Question"
        )


        st.write(
            card["question"]
        )


        st.write("")


        if st.button(
            "Show Answer",
            use_container_width=True
        ):

            st.session_state.show_answer = True



        if st.session_state.show_answer:


            st.divider()


            st.markdown(
                "### Answer"
            )


            st.write(
                card["answer"]
            )



    st.write("")


    # Navigation

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )


    with col1:

        if st.button(
            "Previous",
            use_container_width=True
        ):

            if index > 0:

                st.session_state.card_index -= 1

                st.session_state.show_answer = False

                st.rerun()



    with col3:

        if st.button(
            "Next",
            use_container_width=True
        ):

            if index < total - 1:

                st.session_state.card_index += 1

                st.session_state.show_answer = False

                st.rerun()



    st.divider()


    # PDF Download

    st.subheader(
        "Export Flashcards"
    )


    pdf_file = create_flashcard_pdf(
        cards
    )


    st.download_button(

        label="Download Flashcards PDF",

        data=pdf_file,

        file_name="NEX-01_Flashcards.pdf",

        mime="application/pdf",

        use_container_width=True
    )