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

    # Build PDF into memory
    doc.build(story)

    # Move to beginning of buffer
    buffer.seek(0)

    # Return actual PDF bytes
    return buffer.getvalue()