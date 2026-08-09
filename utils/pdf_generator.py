
from io import BytesIO
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm


# =========================================================
# HELPER
# =========================================================

def format_markdown(text):
    """
    Convert basic Markdown formatting into
    ReportLab-compatible formatting.
    """

    text = str(text)

    # Escape XML-sensitive characters
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    # Bold: **text**
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )

    # Italic: *text*
    text = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        r"<i>\1</i>",
        text
    )

    # Inline code: `text`
    text = re.sub(
        r"`([^`]+)`",
        r"<font name='Courier'>\1</font>",
        text
    )

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

        if line in (
            "---",
            "***",
            "___"
        ):

            continue

        if line.startswith("### "):

            story.append(
                Paragraph(
                    format_markdown(
                        line[4:].strip()
                    ),
                    subheading_style
                )
            )

            continue

        if line.startswith("## "):

            story.append(
                Paragraph(
                    format_markdown(
                        line[3:].strip()
                    ),
                    heading_style
                )
            )

            continue

        if line.startswith("# "):

            story.append(
                Paragraph(
                    format_markdown(
                        line[2:].strip()
                    ),
                    title_style
                )
            )

            continue

        if (
            line.startswith("* ")
            or line.startswith("- ")
        ):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    "• " + format_markdown(text),
                    bullet_style
                )
            )

            continue

        story.append(
            Paragraph(
                format_markdown(line),
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
                f"{index}. "
                f"{format_markdown(question_text)}",
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
                            f"{format_markdown(option)}",
                            option_style
                        )
                    )

        if answer:

            story.append(
                Paragraph(
                    "<b>Correct Answer:</b> "
                    f"{format_markdown(answer)}",
                    answer_style
                )
            )

        if explanation:

            story.append(
                Paragraph(
                    "<b>Explanation:</b> "
                    f"{format_markdown(explanation)}",
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
                f"{index}. "
                f"{format_markdown(question)}",
                question_style
            )
        )

        if answer:

            story.append(
                Paragraph(
                    "<b>Answer:</b> "
                    f"{format_markdown(answer)}",
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
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
    )

    answer_style = ParagraphStyle(
        "ChatAnswer",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        "ChatBullet",
        parent=answer_style,
        leftIndent=15,
        firstLineIndent=-8,
        spaceAfter=4,
    )

    story = []

    story.append(
        Paragraph(
            "NEX-01 AI Study Chat",
            title_style
        )
    )

    # =====================================================
    # LIST CHAT HISTORY
    # =====================================================

    if isinstance(chat_history, list):

        for index, item in enumerate(
            chat_history,
            start=1
        ):

            if not isinstance(item, dict):

                continue

            question = (
                item.get("question")
                or item.get("user")
                or item.get("query")
                or ""
            )

            answer = (
                item.get("answer")
                or item.get("assistant")
                or item.get("response")
                or ""
            )

            # ---------------------------------------------
            # QUESTION
            # ---------------------------------------------

            if question:

                question_text = format_markdown(
                    question
                )

                story.append(
                    Paragraph(
                        f"<b>Question {index}:</b> "
                        f"{question_text}",
                        question_style
                    )
                )

            # ---------------------------------------------
            # ANSWER
            # ---------------------------------------------

            if answer:

                answer = str(answer)

                for line in answer.split("\n"):

                    line = line.strip()

                    if not line:

                        story.append(
                            Spacer(1, 4)
                        )

                        continue

                    # Ignore markdown separators
                    if line in (
                        "---",
                        "***",
                        "___"
                    ):

                        continue

                    # -------------------------------------
                    # BULLET
                    # -------------------------------------

                    if (
                        line.startswith("- ")
                        or line.startswith("* ")
                    ):

                        bullet_text = line[2:].strip()

                        bullet_text = format_markdown(
                            bullet_text
                        )

                        story.append(
                            Paragraph(
                                f"• {bullet_text}",
                                bullet_style
                            )
                        )

                    # -------------------------------------
                    # NUMBERED LIST
                    # -------------------------------------

                    elif re.match(
                        r"^\d+\.\s+",
                        line
                    ):

                        formatted_line = (
                            format_markdown(line)
                        )

                        story.append(
                            Paragraph(
                                formatted_line,
                                answer_style
                            )
                        )

                    # -------------------------------------
                    # NORMAL TEXT
                    # -------------------------------------

                    else:

                        formatted_line = (
                            format_markdown(line)
                        )

                        story.append(
                            Paragraph(
                                formatted_line,
                                answer_style
                            )
                        )

    # =====================================================
    # SINGLE STRING CHAT HISTORY
    # =====================================================

    else:

        chat_history = str(
            chat_history
        )

        for line in chat_history.split("\n"):

            line = line.strip()

            if not line:

                story.append(
                    Spacer(1, 4)
                )

                continue

            formatted_line = format_markdown(
                line
            )

            story.append(
                Paragraph(
                    formatted_line,
                    answer_style
                )
            )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()

