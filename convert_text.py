from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import html

def convert_text_to_pdf(text_content, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18
    )
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    
    story = []
    lines = text_content.splitlines()
    for line in lines:
        if line.strip() == "":
            story.append(Spacer(1, 12))
        else:
            safe_text = html.escape(line)
            p = Paragraph(safe_text, styleN)
            story.append(p)
            story.append(Spacer(1, 6))
    doc.build(story)