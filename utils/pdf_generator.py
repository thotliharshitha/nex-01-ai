
from io import BytesIO
import re
from html import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import mm


# =========================================================
# HELPER FUNCTION
# =========================================================

def clean_text(text):
    """
    Clean text before putting it into a PDF.
    Removes Markdown bold markers and safely handles HTML.
    """

    text = str(text)

    # Remove Markdown bold
    text = text.replace("**", "")

    # Remove Markdown italic markers
    text = text.replace("__", "")

    # Escape HTML characters
    text = escape(text)

    # Preserve line breaks
    text = text.replace("\n", "<br/>")

    return text


# =========================================================
# SUMMARY PDF
# =========================================================

def create_summary_pdf(summary):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "SummaryTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SummaryHeading",
        parent=styles["Heading1"],
        fontSize=15,
        leading=19,
        spaceBefore=12,
        spaceAfter=8,
    )

    subheading_style = ParagraphStyle(
        "SummarySubHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        spaceBefore=8,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "SummaryBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "SummaryBullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-8,
    )

    story = []

    if isinstance(summary, list):

        parts = []

        for item in summary:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                parts.append(item)

        summary = "\n".join(parts)

    summary = str(summary)

    for line in summary.split("\n"):

        line = line.strip()

        if not line:
            story.append(
                Spacer(1, 5)
            )
            continue

        if line in ("---", "***", "___"):
            continue

        if line.startswith("### "):

            story.append(
                Paragraph(
                    clean_text(line[4:].strip()),
                    subheading_style
                )
            )

            continue

        if line.startswith("## "):

            story.append(
                Paragraph(
                    clean_text(line[3:].strip()),
                    heading_style
                )
            )

            continue

        if line.startswith("# "):

            story.append(
                Paragraph(
                    clean_text(line[2:].strip()),
                    title_style
                )
            )

            continue

        if line.startswith("* ") or line.startswith("- "):

            text = line[2:].strip()

            text = clean_text(text)

            story.append(
                Paragraph(
                    "• " + text,
                    bullet_style
                )
            )

            continue

        text = clean_text(line)

        story.append(
            Paragraph(
                text,
                body_style
            )
        )

    if not story:

        story.append(
            Paragraph(
                "No summary available.",
                body_style
            )
        )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# QUIZ PDF
# =========================================================

def create_quiz_pdf(quiz):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "QuizTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=20,
    )

    question_style = ParagraphStyle(
        "QuizQuestion",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    option_style = ParagraphStyle(
        "QuizOption",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        leftIndent=15,
        spaceAfter=4,
    )

    answer_style = ParagraphStyle(
        "QuizAnswer",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceBefore=4,
        spaceAfter=4,
    )

    explanation_style = ParagraphStyle(
        "QuizExplanation",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=10,
    )

    story = []

    story.append(
        Paragraph(
            "NEX-01 AI Quiz",
            title_style
        )
    )

    if not isinstance(quiz, list):
        quiz = []

    for index, question in enumerate(
        quiz,
        start=1
    ):

        if not isinstance(question, dict):
            continue

        question_text = str(
            question.get(
                "question",
                ""
            )
        )

        options = question.get(
            "options",
            []
        )

        answer = str(
            question.get(
                "answer",
                ""
            )
        )

        explanation = str(
            question.get(
                "explanation",
                ""
            )
        )

        story.append(
            Paragraph(
                f"{index}. {clean_text(question_text)}",
                question_style
            )
        )

        if isinstance(options, list):

            letters = [
                "A",
                "B",
                "C",
                "D"
            ]

            for option_index, option in enumerate(
                options
            ):

                if option_index < 4:

                    story.append(
                        Paragraph(
                            f"{letters[option_index]}. "
                            f"{clean_text(option)}",
                            option_style
                        )
                    )

        if answer:

            story.append(
                Paragraph(
                    f"<b>Correct Answer:</b> "
                    f"{clean_text(answer)}",
                    answer_style
                )
            )

        if explanation:

            story.append(
                Paragraph(
                    f"<b>Explanation:</b> "
                    f"{clean_text(explanation)}",
                    explanation_style
                )
            )

    if len(story) == 1:

        story.append(
            Paragraph(
                "No quiz questions available.",
                answer_style
            )
        )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# FLASHCARDS PDF
# =========================================================

def create_flashcard_pdf(flashcards):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "FlashcardTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=20,
    )

    question_style = ParagraphStyle(
        "FlashcardQuestion",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    answer_style = ParagraphStyle(
        "FlashcardAnswer",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=14,
    )

    story = []

    story.append(
        Paragraph(
            "NEX-01 AI Flashcards",
            title_style
        )
    )

    if not isinstance(flashcards, list):
        flashcards = []

    card_number = 0

    for card in flashcards:

        if not isinstance(card, dict):
            continue

        question = str(
            card.get(
                "question",
                ""
            )
        ).strip()

        answer = str(
            card.get(
                "answer",
                ""
            )
        ).strip()

        if not question:
            continue

        card_number += 1

        story.append(
            Paragraph(
                f"{card_number}. "
                f"{clean_text(question)}",
                question_style
            )
        )

        if answer:

            story.append(
                Paragraph(
                    f"<b>Answer:</b> "
                    f"{clean_text(answer)}",
                    answer_style
                )
            )

    if card_number == 0:

        story.append(
            Paragraph(
                "No flashcards available.",
                answer_style
            )
        )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# CHAT PDF
# =========================================================

def create_chat_pdf(chat_history):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ChatTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=20,
    )

    question_style = ParagraphStyle(
        "ChatQuestion",
        parent=styles["Heading2"],
        fontSize=11,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    answer_style = ParagraphStyle(
        "ChatAnswer",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=14,
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "NEX-01 AI Study Chat",
            title_style
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # Make sure chat history is a list
    if not isinstance(chat_history, list):

        chat_history = []

    question_number = 0

    # Process every chat message
    for chat in chat_history:

        if not isinstance(chat, dict):
            continue

        role = chat.get(
            "role",
            ""
        )

        message = chat.get(
            "message",
            ""
        )

        if not message:
            continue

        message = clean_text(message)

        # ---------------------------------------------
        # USER QUESTION
        # ---------------------------------------------

        if role == "user":

            question_number += 1

            story.append(
                Paragraph(
                    f"<b>Question {question_number}:</b>",
                    question_style
                )
            )

            story.append(
                Paragraph(
                    message,
                    answer_style
                )
            )

        # ---------------------------------------------
        # AI ANSWER
        # ---------------------------------------------

        elif role == "assistant":

            story.append(
                Paragraph(
                    "<b>NEX-01 AI:</b>",
                    question_style
                )
            )

            story.append(
                Paragraph(
                    message,
                    answer_style
                )
            )

    # No chat available
    if question_number == 0:

        story.append(
            Paragraph(
                "No chat messages available.",
                answer_style
            )
        )

    # Build PDF
    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()

