import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

def generate_report(memory, filename="Interview_Report.pdf"):
    # Target path setup
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#4F46E5")
    text_color = colors.HexColor("#1E293B")
    muted_color = colors.HexColor("#64748B")
    bg_light = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#E2E8F0")

    # Define custom paragraph styles with appropriate leading
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=muted_color,
        spaceAfter=25
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=text_color,
        spaceAfter=8
    )

    bold_body_style = ParagraphStyle(
        "DocBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    italic_body_style = ParagraphStyle(
        "DocBodyItalic",
        parent=body_style,
        fontName="Helvetica-Oblique"
    )

    callout_style = ParagraphStyle(
        "Callout",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("HireReady-AI Candidate Evaluation", title_style))
    date_str = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Detailed Interview Feedback Report & Analytics • Generated on {date_str}", subtitle_style))
    story.append(Spacer(1, 10))

    # Scorecard Table
    st_score = memory.get("technical_score", 70)
    co_score = memory.get("communication_score", 70)
    cf_score = memory.get("confidence_score", 70)
    avg_score = int((st_score + co_score + cf_score) / 3)

    data = [
        [
            Paragraph("<b>Evaluation Category</b>", bold_body_style), 
            Paragraph("<b>Score Rating</b>", bold_body_style), 
            Paragraph("<b>Performance Benchmark</b>", bold_body_style)
        ],
        [
            Paragraph("Technical Skills Depth", body_style), 
            Paragraph(f"{st_score}%", bold_body_style), 
            Paragraph("Solid technical knowledge demonstrated" if st_score >= 75 else "Foundational understanding; needs practice", body_style)
        ],
        [
            Paragraph("Communication Effectiveness", body_style), 
            Paragraph(f"{co_score}%", bold_body_style), 
            Paragraph("Clear articulation and structure" if co_score >= 75 else "Minor clarity or structured thoughts gaps", body_style)
        ],
        [
            Paragraph("Confidence & Delivery", body_style), 
            Paragraph(f"{cf_score}%", bold_body_style), 
            Paragraph("Calm presence and structured flow" if cf_score >= 75 else "Occasional hesitation noted", body_style)
        ],
        [
            Paragraph("<b>Weighted Interview Score</b>", bold_body_style), 
            Paragraph(f"<b>{avg_score}%</b>", bold_body_style), 
            Paragraph("<b>PASSED MOCK BENCHMARK</b>" if avg_score >= 75 else "<b>RECOMMENDED ADDITIONAL PRACTICE</b>", bold_body_style)
        ]
    ]

    score_table = Table(data, colWidths=[200, 100, 230])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, border_color),
        ('LINEBELOW', (0,-1), (-1,-1), 1.5, primary_color),
        ('BACKGROUND', (0,-1), (-1,-1), bg_light),
    ]))
    
    story.append(Paragraph("Interview Scorecard Dashboard", section_heading))
    story.append(score_table)
    story.append(Spacer(1, 15))

    # Overall Summary Feedback
    overall_feedback = memory.get("overall_feedback", "N/A")
    story.append(Paragraph("General Evaluation Summary", section_heading))
    story.append(Paragraph(overall_feedback, body_style))
    story.append(Spacer(1, 10))

    # Topic Lists - Two Column Layout
    strong_topics = ", ".join(memory.get("strong_topics", []))
    weak_topics = ", ".join(memory.get("weak_topics", []))
    mistakes = memory.get("mistakes", [])
    recommendations = memory.get("recommended_topics", [])

    topics_data = [
        [
            Paragraph("<b>Demonstrated Strong Topics</b>", bold_body_style),
            Paragraph("<b>Identified Weak Topics</b>", bold_body_style)
        ],
        [
            Paragraph(strong_topics if strong_topics else "None recorded", body_style),
            Paragraph(weak_topics if weak_topics else "None recorded", body_style)
        ]
    ]
    
    topics_table = Table(topics_data, colWidths=[260, 270])
    topics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,1), (-1,1), 0.5, border_color),
    ]))
    
    story.append(Paragraph("Demonstrated Skills & Topic Breakdown", section_heading))
    story.append(topics_table)
    story.append(Spacer(1, 15))

    # Mistakes and Study Recommendations
    recs_data = [
        [
            Paragraph("<b>Recorded Mistakes / Conception Gaps</b>", bold_body_style),
            Paragraph("<b>Actionable Study Plan Topics</b>", bold_body_style)
        ],
        [
            Paragraph("<br/>".join(f"• {m}" for m in mistakes) if mistakes else "No critical technical errors recorded.", body_style),
            Paragraph("<br/>".join(f"• {r}" for r in recommendations) if recommendations else "No specific study topics suggested.", body_style)
        ]
    ]

    recs_table = Table(recs_data, colWidths=[260, 270])
    recs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), bg_light),
        ('LINEBELOW', (0,0), (-1,0), 1, primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,1), (-1,1), 0.5, border_color),
    ]))
    story.append(Paragraph("Constructive Feedback & Study Guide", section_heading))
    story.append(recs_table)
    
    # Page Break before Transcript Review
    qa_review = memory.get("qa_review", [])
    if qa_review:
        story.append(PageBreak())
        story.append(Paragraph("Detailed Question-by-Question Evaluation", section_heading))
        story.append(Spacer(1, 5))
        
        for idx, qa in enumerate(qa_review):
            q_num = idx + 1
            score = qa.get("score", 0)
            
            story.append(Paragraph(f"<b>Question {q_num}</b> (Score: {score}/100)", bold_body_style))
            story.append(Paragraph(f"<i>Q: {qa.get('question', '')}</i>", italic_body_style))
            story.append(Paragraph(f"Candidate Response: \"{qa.get('answer', '')}\"", callout_style))
            
            # Sub-analysis table for strengths and gaps
            qa_sub_data = [
                [
                    Paragraph("<b>Key Strengths</b>", bold_body_style),
                    Paragraph("<b>Areas to Improve</b>", bold_body_style)
                ],
                [
                    Paragraph(qa.get('strengths', 'N/A'), body_style),
                    Paragraph(qa.get('gaps', 'N/A'), body_style)
                ]
            ]
            qa_sub_table = Table(qa_sub_data, colWidths=[260, 270])
            qa_sub_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
                ('LINEBELOW', (0,0), (-1,0), 0.5, primary_color),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LINEBELOW', (0,1), (-1,1), 0.5, border_color),
            ]))
            story.append(qa_sub_table)
            story.append(Spacer(1, 5))
            
            # Ideal response guidance
            story.append(Paragraph(f"<b>Recommended Ideal Answer:</b>", bold_body_style))
            story.append(Paragraph(qa.get('ideal_answer', 'N/A'), body_style))
            story.append(Spacer(1, 15))
            
    doc.build(story)