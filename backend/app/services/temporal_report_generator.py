import os
from statistics import mean
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from app.core.config import settings
from app.services.analysis_writer import load_analysis
from reportlab.platypus import Image


def generate_temporal_pdf(
    report_id: str,
    overall_score: float,
    flagging_result: dict,
    processing_time: float,
    thumbnails: list
):

    os.makedirs(settings.REPORT_FOLDER, exist_ok=True)
    pdf_path = os.path.join(settings.REPORT_FOLDER, f"{report_id}_v2.pdf")

    analysis = load_analysis(report_id)
    frame_results = analysis["frame_results"]
    metadata = analysis["video_metadata"]

    scores = [f["score"] for f in frame_results]

    worst_score = min(scores)
    best_score = max(scores)
    avg_score = round(mean(scores), 2)

    doc = SimpleDocTemplate(pdf_path)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    # Title
    elements.append(Paragraph("Posture Analysis Report (Temporal v2)", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Metadata Table
    data = [
        ["Report ID", report_id],
        ["Duration (seconds)", metadata["duration_seconds"]],
        ["Frames Analyzed", len(frame_results)],
        ["Processing Time (s)", processing_time],
        ["Overall Weighted Score", overall_score],
        ["Percent Time in Bad Posture", f'{flagging_result["percent_time_bad"]}%'],
        ["Worst Score", worst_score],
        ["Best Score", best_score],
        ["Average Score", avg_score]
    ]

    table = Table(data, colWidths=[2.5 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    # Flagged Events Section
    elements.append(Paragraph("Flagged Posture Events", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    if flagging_result["events"]:
        event_list = []

        for event in flagging_result["events"]:
            text = f'Timestamp: {event["timestamp"]} sec | Score: {event["score"]} | Issue: {event["primary_issue"]}'
            event_list.append(ListItem(Paragraph(text, normal_style)))

        elements.append(ListFlowable(event_list, bulletType='bullet'))

    else:
        elements.append(Paragraph("No significant posture deviations detected.", normal_style))

    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Visual Evidence", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    for thumb in thumbnails:

        img = Image(thumb["path"], width=4*inch, height=3*inch)
        elements.append(img)

        caption = f'Timestamp: {thumb["timestamp"]}s | Score: {thumb["score"]} | Issue: {thumb["issue"]}'
        elements.append(Paragraph(caption, normal_style))
        elements.append(Spacer(1, 0.4 * inch))
    doc.build(elements)

    return pdf_path