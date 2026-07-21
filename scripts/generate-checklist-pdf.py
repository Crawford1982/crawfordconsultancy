"""Generate the branded First Employee Checklist PDF."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "downloads" / "first-employee-checklist.pdf"
LOGO = ROOT / "logo.png"

INK = colors.HexColor("#1a1f2e")
SAGE = colors.HexColor("#3d7a6b")
SAGE_L = colors.HexColor("#f4f9f8")
STONE = colors.HexColor("#c8a96e")
MID = colors.HexColor("#4a5568")
MUTED = colors.HexColor("#8896aa")
WHITE = colors.white
CHECK_BORDER = colors.HexColor("#c5ced6")

PAGE_W, PAGE_H = A4
MARGIN_L = 14 * mm
MARGIN_R = 14 * mm
MARGIN_T = 14 * mm
MARGIN_B = 14 * mm
COL_WIDTH = 88 * mm
COL_GAP = 6 * mm


def checkbox_cell():
    box = Table([[""]], colWidths=[4 * mm], rowHeights=[4 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.55, CHECK_BORDER),
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return box


def item_row(text, styles, text_width):
    row = Table(
        [[checkbox_cell(), Paragraph(text, styles["item"])]],
        colWidths=[5.5 * mm, text_width],
    )
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ]
        )
    )
    return row


def section_table(title, items, styles, width):
    rows = [[Paragraph(title, styles["section"])]]
    for item in items:
        rows.append([item_row(item, styles, width - 5.5 * mm)])

    table = Table(rows, colWidths=[width])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SAGE_L),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("TOPPADDING", (0, 1), (-1, -1), 3),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, 0), 0.75, colors.HexColor("#d8e8e4")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e4e2dc")),
            ]
        )
    )
    return table


def stack_sections(sections, styles, width, gap=3.5 * mm):
    rows = []
    for index, (title, items) in enumerate(sections):
        rows.append([section_table(title, items, styles, width)])
        if index < len(sections) - 1:
            rows.append([Spacer(1, gap)])
    return Table(rows, colWidths=[width])


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#e4e2dc"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, 11 * mm, PAGE_W - MARGIN_R, 11 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        MARGIN_L,
        7 * mm,
        "Crawford Consultancy  ·  crawfordconsultancy.co.uk  ·  hello@crawfordconsultancy.co.uk",
    )
    canvas.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    return {
        "badge": ParagraphStyle(
            "badge",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            textColor=STONE,
            alignment=TA_CENTER,
            spaceAfter=4,
            letterSpacing=1.1,
        ),
        "title": ParagraphStyle(
            "title",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=21,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12,
            textColor=SAGE,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "intro": ParagraphStyle(
            "intro",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=MID,
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "section": ParagraphStyle(
            "section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=INK,
        ),
        "item": ParagraphStyle(
            "item",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=MID,
        ),
        "cta_title": ParagraphStyle(
            "cta_title",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=3,
        ),
        "cta_body": ParagraphStyle(
            "cta_body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#d8dde6"),
            alignment=TA_CENTER,
        ),
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title="First Employee Checklist",
        author="Crawford Consultancy",
        subject="UK checklist for hiring your first employee",
    )

    story = []

    logo = Image(str(LOGO), width=18 * mm, height=18 * mm)
    logo.hAlign = "CENTER"
    story.extend(
        [
            Spacer(1, 2 * mm),
            logo,
            Spacer(1, 4 * mm),
            Paragraph("FREE DOWNLOAD", styles["badge"]),
            Paragraph("First Employee Checklist", styles["title"]),
            Paragraph("Everything you need before your new employee starts", styles["subtitle"]),
            Paragraph(
                "<b>Congratulations on taking the next step in growing your business!</b> "
                "Use this checklist to make sure you&rsquo;ve covered the essentials before welcoming your first employee.",
                styles["intro"],
            ),
            Spacer(1, 5 * mm),
        ]
    )

    left_sections = [
        (
            "Planning",
            [
                "Decide exactly what role you need.",
                "Set the salary and working hours.",
                "Prepare a job description.",
                "Decide how you&rsquo;ll recruit.",
            ],
        ),
        (
            "Becoming an Employer",
            [
                "Register as an employer with HMRC.",
                "Arrange Employers&rsquo; Liability Insurance.",
            ],
        ),
        (
            "Before They Start",
            [
                "Complete a Right to Work check.",
                "Issue an employment contract.",
                "Agree a start date.",
                "Collect bank details.",
                "Obtain their National Insurance number (if available).",
                "Ask them to complete a new starter form.",
            ],
        ),
        (
            "Payroll &amp; Pensions",
            [
                "Set up payroll.",
                "Register the employee for payroll.",
                "Understand your workplace pension responsibilities.",
                "Keep payroll records.",
            ],
        ),
    ]

    right_sections = [
        (
            "HR Documents",
            [
                "Prepare an Employee Handbook (if applicable).",
                "Have your key workplace policies in place.",
            ],
        ),
        (
            "First Day",
            [
                "Prepare their workstation and equipment.",
                "Plan their induction.",
                "Introduce them to the team.",
                "Provide Health and Safety information.",
                "Explain company procedures and expectations.",
            ],
        ),
        (
            "Employee Records",
            [
                "Employment contract filed.",
                "Right to Work documents copied.",
                "Emergency contact details recorded.",
                "HMRC starter information retained.",
                "Payroll records established.",
                "Workplace pension records established.",
                "Annual leave record created.",
                "Sickness absence record created.",
                "Training record started.",
                "Probation review dates diarised.",
            ],
        ),
    ]

    left_col = stack_sections(left_sections, styles, COL_WIDTH)
    right_col = stack_sections(right_sections, styles, COL_WIDTH)
    grid = Table([[left_col, right_col]], colWidths=[COL_WIDTH, COL_WIDTH], hAlign="CENTER")
    grid.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), COL_GAP / 2),
                ("LEFTPADDING", (1, 0), (-1, -1), COL_GAP / 2),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(grid)

    story.append(Spacer(1, 5 * mm))
    cta = Table(
        [
            [Paragraph("Need some support?", styles["cta_title"])],
            [
                Paragraph(
                    "Crawford Consultancy can help with employment contracts, payroll administration, "
                    "employee handbooks, HR documentation, workplace policies and ongoing HR support.<br/>"
                    "<b>crawfordconsultancy.co.uk/contact</b>",
                    styles["cta_body"],
                )
            ],
        ],
        colWidths=[PAGE_W - MARGIN_L - MARGIN_R],
        hAlign="CENTER",
    )
    cta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), INK),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
            ]
        )
    )
    story.append(cta)

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
