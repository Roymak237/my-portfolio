from __future__ import annotations

from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


@dataclass(frozen=True)
class CvData:
    name: str
    headline: str
    location: str
    email: str
    phone: str
    github: str
    portfolio: str


def _bullet_list(items: list[str], bullet_font_size: int = 9) -> ListFlowable:
    styles = getSampleStyleSheet()
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["BodyText"],
        fontSize=bullet_font_size,
        leading=12,
        spaceAfter=2,
    )
    return ListFlowable(
        [ListItem(Paragraph(text, bullet_style)) for text in items],
        bulletType="bullet",
        start="bullet",
        leftIndent=14,
        bulletFontSize=9,
    )


def build_cv_pdf(output_path: str) -> None:
    data = CvData(
        name="FRU CHI EHUD NEBA",
        headline="Systems & Network Engineer (Linux/DevOps) | Backend Developer",
        location="Remote / Africa (Open to relocation)",
        email="ehudneba@example.com",
        phone="+237 672 504 126 (WhatsApp)",
        github="github.com/Roymak237",
        portfolio="roymak237.github.io/portfolio",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        spaceAfter=6,
        textColor=colors.HexColor("#111827"),
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=10,
        textColor=colors.HexColor("#374151"),
    )
    section = ParagraphStyle(
        "Section",
        parent=styles["Heading3"],
        fontSize=11,
        leading=14,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.HexColor("#111827"),
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#111827"),
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#374151"),
    )

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.2 * cm,
        title=f"{data.name} - CV",
        author=data.name,
    )

    story: list[object] = []

    story.append(Paragraph(data.name, title))
    story.append(Paragraph(data.headline, subtitle))

    contact_table = Table(
        [
            [
                Paragraph(f"<b>Location:</b> {data.location}", small),
                Paragraph(f"<b>Email:</b> {data.email}", small),
            ],
            [
                Paragraph(f"<b>Phone:</b> {data.phone}", small),
                Paragraph(f"<b>GitHub:</b> {data.github}  &nbsp;&nbsp; <b>Portfolio:</b> {data.portfolio}", small),
            ],
        ],
        colWidths=[8.7 * cm, 8.7 * cm],
        hAlign="LEFT",
    )
    contact_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(contact_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Professional Summary", section))
    story.append(
        Paragraph(
            "Hands-on Systems &amp; Network Engineer with strong Linux fundamentals and a backend mindset. "
            "I build secure, maintainable systems, automate repetitive work with scripts, and develop REST APIs "
            "that support modern web and mobile applications.",
            body,
        )
    )

    story.append(Paragraph("Core Skills", section))
    story.append(
        _bullet_list(
            [
                "Linux administration, user &amp; permissions management, troubleshooting",
                "System hardening basics and secure operational practices",
                "Networking fundamentals (TCP/IP, DNS, HTTP/HTTPS) and service configuration",
                "Automation &amp; scripting: Python, Bash-style workflows",
                "Backend development: REST APIs with Python &amp; Flask",
                "Databases &amp; tooling: SQL basics, Git, Firebase integration",
            ]
        )
    )

    story.append(Paragraph("Certifications", section))
    story.append(
        _bullet_list(
            [
                "Linux Cloud &amp; DevOps — Certificate of completion",
                "Linux Specialization Course — Certificate of completion",
                "Managing Linux Systems — Certificate of completion",
                "Securing Linux Systems — Certificate of completion",
            ]
        )
    )

    story.append(Paragraph("Projects", section))
    story.append(
        _bullet_list(
            [
                "<b>Edu Papers</b> — Built a web/mobile solution for sharing past exam papers and notes; implemented authentication, file sharing, and search-friendly structure.",
                "<b>Grid Survival</b> — Collaborated on a 2D survival game using Python and Pygame; focused on core gameplay and stability.",
                "<b>Database Management System</b> — Implemented data structures and query-focused workflows to understand DB fundamentals and performance.",
            ]
        )
    )

    story.append(Paragraph("Education", section))
    story.append(
        _bullet_list(
            [
                "<b>ICT University (ICT-U)</b> — Level 3 Student",
            ]
        )
    )

    story.append(Spacer(1, 6))
    story.append(
        Paragraph(
            "Availability: Immediate • Preferred roles: Systems/Network Engineer, Linux/DevOps Intern/Junior, Backend Developer",
            small,
        )
    )

    def on_page(canvas, _doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
        canvas.setLineWidth(0.6)
        canvas.line(doc.leftMargin, A4[1] - doc.topMargin + 8, A4[0] - doc.rightMargin, A4[1] - doc.topMargin + 8)
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


if __name__ == "__main__":
    build_cv_pdf("cv.pdf")

