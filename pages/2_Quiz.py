import streamlit as st

from utils.pdf_reader import extract_text
from utils.quiz import generate_quiz
from utils.pdf_generator import create_quiz_pdf


st.set_page_config(
    page_title="AI Quiz",
    layout="wide"
)


st.title("NEX-01 AI Quiz")

st.caption(
    "Test your understanding with AI-generated questions from your document."
)


st.divider()


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file:

    pdf_name = uploaded_file.name

    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = ""

    if st.session_state.pdf_name != pdf_name:

        st.session_state.pdf_name = pdf_name

        if "quiz" in st.session_state:
            del st.session_state.quiz

    text = extract_text(uploaded_file)

    st.success(
        "PDF uploaded successfully"
    )

    if "quiz" not in st.session_state:

        with st.spinner(
            "Generating quiz..."
        ):

            st.session_state.quiz = generate_quiz(text)

    quiz = st.session_state.quiz

    if not quiz:

        st.error(
            "Quiz generation failed. Try another PDF."
        )

    else:

        st.subheader(
            "Answer the questions"
        )

        st.write(
            f"Total Questions: {len(quiz)}"
        )

        answers = {}

        for i, q in enumerate(quiz):

            with st.container(border=True):

                st.markdown(
                    f"### Question {i+1} of {len(quiz)}"
                )

                answers[i] = st.radio(
                    q["question"],
                    q["options"],
                    index=None,
                    key=f"question_{i}"
                )

        st.divider()

        if st.button(
            "Submit Quiz",
            use_container_width=True
        ):

            if None in answers.values():

                st.warning(
                    "Please answer all questions before submitting."
                )

                st.stop()

            score = 0

            st.divider()

            st.subheader(
                "Quiz Result"
            )

            for i, q in enumerate(quiz):

                if answers[i] == q["answer"]:

                    score += 1

                    st.success(
                        f"Question {i+1}: Correct"
                    )

                else:

                    st.error(
                        f"Question {i+1}: Wrong"
                    )

                st.write(
                    f"Correct Answer: **{q['answer']}**"
                )

                with st.container(border=True):

                    st.write(
                        q["explanation"]
                    )

            st.divider()

            percentage = (
                score / len(quiz)
            ) * 100

            st.success(
                f"Final Score: {score}/{len(quiz)}"
            )

            st.info(
                f"Percentage: {percentage:.0f}%"
            )

            if percentage >= 80:

                st.success(
                    "Excellent Performance"
                )

            elif percentage >= 50:

                st.warning(
                    "Good Performance"
                )

            else:

                st.error(
                    "Keep Practicing"
                )

            st.divider()

            pdf = create_quiz_pdf(quiz)

            st.download_button(
                label="Download Quiz PDF",
                data=pdf,
                file_name="NEX-01_AI_Quiz.pdf",
                mime="application/pdf",
                use_container_width=True
            )