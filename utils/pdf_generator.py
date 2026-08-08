from io import BytesIO
import re

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

    # Convert Gemini list response to string
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

    # Process summary line by line
    for line in summary.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        # Remove markdown horizontal lines
        if line in ("---", "***", "___"):
            continue

        # H3
        if line.startswith("### "):

            text = line[4:].strip()

            story.append(
                Paragraph(
                    text,
                    subheading_style
                )
            )

            continue

        # H2
        if line.startswith("## "):

            text = line[3:].strip()

            story.append(
                Paragraph(
                    text,
                    heading_style
                )
            )

            continue

        # H1
        if line.startswith("# "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    text,
                    title_style
                )
            )

            continue

        # Bullet points
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

        # Normal text
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

    # Make sure quiz is a list
    if not isinstance(quiz, list):
        quiz = []

    for index, question in enumerate(quiz, start=1):

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

        # Question
        story.append(
            Paragraph(
                f"{index}. {question_text}",
                question_style
            )
        )

        # Options
        if isinstance(options, list):

            for option_index, option in enumerate(
                options
            ):

                letters = [
                    "A",
                    "B",
                    "C",
                    "D"
                ]

                if option_index < 4:

                    story.append(
                        Paragraph(
                            f"{letters[option_index]}. {option}",
                            option_style
                        )
                    )

        # Correct answer
        if answer:

            story.append(
                Paragraph(
                    f"<b>Correct Answer:</b> {answer}",
                    answer_style
                )
            )

        # Explanation
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