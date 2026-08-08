from io import BytesIO
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm


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
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading1"],
        fontSize=15,
        leading=19,
        spaceBefore=12,
        spaceAfter=8,
    )

    subheading_style = ParagraphStyle(
        "SubHeadingStyle",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        spaceBefore=8,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-8,
    )

    story = []

    # Gemini may return a list
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
            story.append(Spacer(1, 5))
            continue

        if line in ("---", "***", "___"):
            continue

        if line.startswith("### "):

            story.append(
                Paragraph(
                    line[4:].strip(),
                    subheading_style
                )
            )

            continue

        if line.startswith("## "):

            story.append(
                Paragraph(
                    line[3:].strip(),
                    heading_style
                )
            )

            continue

        if line.startswith("# "):

            story.append(
                Paragraph(
                    line[2:].strip(),
                    title_style
                )
            )

            continue

        if line.startswith("* ") or line.startswith("- "):

            text = line[2:].strip()

            text = re.sub(
                r"\*\*(.*?)\*\*",
                r"<b>\1</b>",
                text
            )

            story.append(
                Paragraph(
                    "• " + text,
                    bullet_style
                )
            )

            continue

        text = re.sub(
            r"\*\*(.*?)\*\*",
            r"<b>\1</b>",
            line
        )

        story.append(
            Paragraph(
                text,
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
        "QuestionStyle",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    option_style = ParagraphStyle(
        "OptionStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        leftIndent=15,
        spaceAfter=4,
    )

    answer_style = ParagraphStyle(
        "AnswerStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceBefore=4,
        spaceAfter=4,
    )

    explanation_style = ParagraphStyle(
        "ExplanationStyle",
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
                f"{index}. {question_text}",
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
                            f"{letters[option_index]}. {option}",
                            option_style
                        )
                    )

        if answer:

            story.append(
                Paragraph(
                    f"<b>Correct Answer:</b> {answer}",
                    answer_style
                )
            )

        if explanation:

            story.append(
                Paragraph(
                    f"<b>Explanation:</b> {explanation}",
                    explanation_style
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

    for index, card in enumerate(
        flashcards,
        start=1
    ):

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

        story.append(
            Paragraph(
                f"{index}. {question}",
                question_style
            )
        )

        if answer:

            story.append(
                Paragraph(
                    f"<b>Answer:</b> {answer}",
                    answer_style
                )
            )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()