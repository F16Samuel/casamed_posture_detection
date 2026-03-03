import os
import logging
from typing import List

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib import fonts

from app.core.config import settings
from app.schemas.posture_response import Metrics

logger = logging.getLogger(__name__)


def generate_pdf_report(
    report_id: str,
    posture_score: float,
    classification: str,
    metrics: Metrics,
    feedback: List[str],
    image_path: str
) -> str:
    """
    Generates a structured posture analysis PDF report.
    """

    pdf_path = os.path.join(settings.REPORT_FOLDER, f"{report_id}.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # ---------------------------------
    # Title
    # ---------------------------------
    title_style = styles["Heading1"]
    elements.append(Paragraph("AI Posture Analysis Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------------------------------
    # Score Section
    # ---------------------------------
    score_style = ParagraphStyle(
        name="ScoreStyle",
        parent=styles["Normal"],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=10
    )

    elements.append(Paragraph(f"<b>Posture Score:</b> {posture_score}", score_style))
    elements.append(Paragraph(f"<b>Classification:</b> {classification}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------------------------------
    # Metrics Table
    # ---------------------------------
    metrics_data = [
        ["Metric", "Value"],
        ["Neck Angle (°)", str(metrics.neck_angle)],
        ["Spine Vertical Deviation (°)", str(metrics.spine_vertical_deviation)],
        ["Shoulder Alignment Difference (%)", str(metrics.shoulder_alignment_difference)],
        ["Hip Alignment Difference (%)", str(metrics.hip_alignment_difference)],
    ]

    table = Table(metrics_data, colWidths=[3.5 * inch, 1.5 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))

    # ---------------------------------
    # Feedback Section
    # ---------------------------------
    elements.append(Paragraph("<b>Posture Feedback:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    for item in feedback:
        elements.append(Paragraph(f"• {item}", styles["Normal"]))
        elements.append(Spacer(1, 0.15 * inch))

    elements.append(Spacer(1, 0.4 * inch))

    # ---------------------------------
    # Skeleton Image
    # ---------------------------------
    if os.path.exists(image_path):
        img = Image(image_path, width=4.5 * inch, height=6 * inch)
        elements.append(Paragraph("<b>Annotated Posture Visualization:</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(img)
        elements.append(Spacer(1, 0.4 * inch))

    # ---------------------------------
    # Disclaimer
    # ---------------------------------
    disclaimer_text = (
        "Disclaimer: This AI-generated posture analysis is intended "
        "for general wellness and informational purposes only. "
        "It is not a medical diagnosis and should not replace consultation "
        "with a qualified healthcare professional."
    )

    elements.append(Paragraph(disclaimer_text, styles["Italic"]))

    # Build PDF
    doc.build(elements)

    logger.info(f"PDF report generated at {pdf_path}")

    return pdf_path