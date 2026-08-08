import streamlit as st

from utils.pdf_reader import extract_text
from utils.summary import generate_summary
from utils.pdf_generator import create_summary_pdf


st.set_page_config(
    page_title="AI Summary",
    layout="wide"
)


st.title("AI Document Summary")

st.caption(
    "Upload your document and generate an AI-powered summary."
)

st.divider()


st.subheader("Upload Your Document")


uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file:

    st.success("PDF uploaded successfully")

    with st.spinner("Reading document..."):

        text = extract_text(uploaded_file)

    st.divider()


    if st.button(
        "Generate Summary",
        use_container_width=True
    ):

        with st.spinner("Generating summary..."):

            summary = generate_summary(text)

        st.session_state["summary"] = summary


if "summary" in st.session_state:

    st.divider()

    st.subheader("Generated Summary")

    with st.container(border=True):

        st.markdown(
            st.session_state["summary"]
        )


    # Create PDF
    pdf = create_summary_pdf(
        st.session_state["summary"]
    )


    # Download PDF
    st.download_button(
        label="Download Summary PDF",
        data=pdf,
        file_name="NEX-01_AI_Summary.pdf",
        mime="application/pdf",
        use_container_width=True
    )