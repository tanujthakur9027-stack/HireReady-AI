import importlib

try:
    reportlab_platypus = importlib.import_module("reportlab.platypus")
    SimpleDocTemplate = getattr(reportlab_platypus, "SimpleDocTemplate", None)
    Paragraph = getattr(reportlab_platypus, "Paragraph", None)
except ImportError:
    SimpleDocTemplate = None
    Paragraph = None

try:
    reportlab_styles = importlib.import_module("reportlab.lib.styles")
    getSampleStyleSheet = getattr(reportlab_styles, "getSampleStyleSheet", None)
except ImportError:
    getSampleStyleSheet = None

styles = getSampleStyleSheet() if getSampleStyleSheet is not None else None


def generate_report(memory, filename):
    if styles is None or SimpleDocTemplate is None or Paragraph is None:
        raise ImportError(
            "reportlab is required to generate PDF reports. "
            "Install it with 'pip install reportlab'."
        )

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b>InterviewMate AI Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Technical Score : {memory.get('technical_score',0)}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Communication Score : {memory.get('communication_score',0)}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Confidence Score : {memory.get('confidence_score',0)}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Strong Topics</b>",
            styles["Heading2"]
        )
    )

    for topic in memory.get("strong_topics",[]):

        story.append(

            Paragraph(

                topic,

                styles["BodyText"]

            )

        )

    story.append(
        Paragraph(
            "<b>Weak Topics</b>",
            styles["Heading2"]
        )
    )

    for topic in memory.get("weak_topics",[]):

        story.append(

            Paragraph(

                topic,

                styles["BodyText"]

            )

        )

    story.append(
        Paragraph(
            "<b>Recommended Topics</b>",
            styles["Heading2"]
        )
    )

    for topic in memory.get("recommended_topics",[]):

        story.append(

            Paragraph(

                topic,

                styles["BodyText"]

            )

        )

    doc.build(story)