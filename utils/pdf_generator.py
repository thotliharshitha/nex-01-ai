from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


styles = getSampleStyleSheet()


# ---------------------------------------------------
# Summary PDF
# ---------------------------------------------------

def create_summary_pdf(summary):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    content = []

    content.append(
        Paragraph(
            "NEX-01 AI Summary",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for line in summary.split("\n"):

        if line.strip():

            content.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

            content.append(
                Spacer(1, 8)
            )

    doc.build(content)

    buffer.seek(0)

    return buffer


# ---------------------------------------------------
# Important Questions PDF
# ---------------------------------------------------

def create_questions_pdf(questions):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    content = []

    content.append(
        Paragraph(
            "NEX-01 Important Questions",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for i, question in enumerate(questions):

        content.append(
            Paragraph(
                f"<b>{i+1}.</b> {question}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

    doc.build(content)

    buffer.seek(0)

    return buffer


# ---------------------------------------------------
# Quiz PDF
# ---------------------------------------------------

def create_quiz_pdf(quiz):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    content = []

    content.append(
        Paragraph(
            "NEX-01 AI Quiz",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for i, item in enumerate(quiz):

        content.append(
            Paragraph(
                f"<b>Question {i+1}</b><br/>{item['question']}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 8)
        )

        for option in item["options"]:

            content.append(
                Paragraph(
                    option,
                    styles["BodyText"]
                )
            )

        content.append(
            Spacer(1, 8)
        )

        content.append(
            Paragraph(
                f"<b>Answer:</b> {item['answer']}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 15)
        )

    doc.build(content)

    buffer.seek(0)

    return buffer


# ---------------------------------------------------
# Flashcards PDF
# ---------------------------------------------------

def create_flashcard_pdf(flashcards):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    content = []

    content.append(
        Paragraph(
            "NEX-01 AI Flashcards",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for i, card in enumerate(flashcards):

        content.append(
            Paragraph(
                f"<b>{i+1}. Question</b><br/>{card['question']}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 8)
        )

        content.append(
            Paragraph(
                f"<b>Answer</b><br/>{card['answer']}",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

    doc.build(content)

    buffer.seek(0)

    return buffer


# ---------------------------------------------------
# Chat PDF
# ---------------------------------------------------

def create_chat_pdf(chat_history):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    content = []

    content.append(
        Paragraph(
            "NEX-01 AI Chat",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for chat in chat_history:

        role = "You" if chat["role"] == "user" else "NEX-01 AI"

        content.append(
            Paragraph(
                f"<b>{role}</b>",
                styles["Heading3"]
            )
        )

        content.append(
            Paragraph(
                chat["message"].replace("\n", "<br/>"),
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

    doc.build(content)

    buffer.seek(0)

    return buffer