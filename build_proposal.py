#!/usr/bin/env python3
"""Generate the Royalty Talent - ORCA Proposal as a PDF, priced in USD (no VAT, US-based)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

NAVY = colors.HexColor("#0B2A4A")
ACCENT = colors.HexColor("#1F7A8C")
LIGHT = colors.HexColor("#EAF2F4")
GREY = colors.HexColor("#5A6B78")

styles = getSampleStyleSheet()

h_title = ParagraphStyle("h_title", parent=styles["Title"], textColor=NAVY,
                         fontSize=24, leading=28, spaceAfter=2)
h_sub = ParagraphStyle("h_sub", parent=styles["Normal"], textColor=GREY,
                       fontSize=11, leading=15, spaceAfter=2)
h_sec = ParagraphStyle("h_sec", parent=styles["Heading2"], textColor=ACCENT,
                       fontSize=13, leading=16, spaceBefore=14, spaceAfter=6,
                       fontName="Helvetica-Bold")
body = ParagraphStyle("body", parent=styles["Normal"], fontSize=10.5,
                      leading=15, textColor=colors.HexColor("#22303A"))
bullet = ParagraphStyle("bullet", parent=body, leftIndent=10, spaceAfter=3)
small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8.5,
                       leading=12, textColor=GREY)
cell = ParagraphStyle("cell", parent=body, fontSize=10)
cell_r = ParagraphStyle("cell_r", parent=cell, alignment=TA_RIGHT)
cell_b = ParagraphStyle("cell_b", parent=cell, fontName="Helvetica-Bold")
cell_rb = ParagraphStyle("cell_rb", parent=cell_r, fontName="Helvetica-Bold")
cell_bw = ParagraphStyle("cell_bw", parent=cell_b, textColor=colors.white)
cell_rbw = ParagraphStyle("cell_rbw", parent=cell_rb, textColor=colors.white)


def build():
    doc = SimpleDocTemplate(
        "Royalty_Talent_ORCA_Proposal_USD.pdf", pagesize=A4,
        leftMargin=22 * mm, rightMargin=22 * mm,
        topMargin=20 * mm, bottomMargin=18 * mm,
        title="Royalty Talent - ORCA Proposal", author="ORCA",
    )
    e = []

    e.append(Paragraph("ORCA Proposal", h_title))
    e.append(Paragraph("Prepared for: <b>Ivan Duschatzky</b> — Royalty Talent", h_sub))
    e.append(Paragraph("Date: 4 June 2026", h_sub))
    e.append(Spacer(1, 6))
    e.append(HRFlowable(width="100%", thickness=1.2, color=LIGHT))

    # Summary
    e.append(Paragraph("Summary", h_sec))
    e.append(Paragraph(
        "ORCA is the structured, expert-led training platform that ramps new recruiters "
        "faster and lifts biller productivity across your team — without you having to "
        "build training in-house.", body))
    e.append(Spacer(1, 6))
    e.append(Paragraph("Your 5-seat ORCA plan secures access to:", body))
    e.append(Spacer(1, 4))
    for t, d in [
        ("Training platform (5 seats)",
         "Short, sharp &amp; impactful expert-led video lessons for recruiters and founders."),
        ("Live monthly group coaching",
         "Expert-led sessions where your team learns and asks questions live."),
        ("New-hire onboarding &amp; ramp system",
         "A structured path that gets brand-new recruiters productive fast."),
        ("Knowledge Hub",
         "Downloadable scripts, frameworks, templates &amp; business assets your team uses on live deals."),
        ("Weekly video lessons with assessments",
         "Self-paced learning with progress tracking for every recruiter."),
        ("Supplier discounts",
         "RecTech, back-office &amp; business solutions."),
    ]:
        e.append(Paragraph(
            f'<font color="#1F7A8C">&#9679;</font> <b>{t}</b> '
            f'— <font color="#1F7A8C"><b>INCLUDED.</b></font> {d}', bullet))

    # Training & coaching
    e.append(Paragraph("Training &amp; Coaching", h_sec))
    e.append(Paragraph("From rookie to senior consultants.", body))
    e.append(Spacer(1, 4))
    steps = ["Video lessons", "Monthly focus topic", "Live group coaching",
             "High-level course modules", "Assessments &amp; assignments", "Apply on the desk"]
    for i, s in enumerate(steps, 1):
        e.append(Paragraph(f"<b>{i}.</b> {s}", bullet))
    e.append(Spacer(1, 6))
    e.append(Paragraph("<b>How a month works:</b>", body))
    for w, d in [
        ("Week 1", "Video lesson + downloadable framework"),
        ("Week 2", "Live expert group coaching session"),
        ("Week 3", "Practice + assessment"),
        ("Week 4", "Review and apply on the desk"),
    ]:
        e.append(Paragraph(
            f'<font color="#1F7A8C">&#9679;</font> <b>{w}:</b> {d}', bullet))

    # Order form
    e.append(Paragraph("Order Form", h_sec))
    e.append(Paragraph("Thank you for choosing ORCA.", body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "In order for us to process your logins and invoice please check the details "
        "below and confirm. The service is provided in line with our standard terms and "
        "conditions, which can be found here: "
        '<a href="https://www.trainwithorca.com/terms-of-service" color="#1F7A8C">'
        "trainwithorca.com/terms-of-service</a>.", body))
    e.append(Spacer(1, 8))

    data = [
        [Paragraph("Description", cell_b), Paragraph("Price", cell_rb),
         Paragraph("Qty", cell_rb), Paragraph("Subtotal", cell_rb)],
        [Paragraph("ORCA (Monthly) — User licences", cell),
         Paragraph("$56.44", cell_r), Paragraph("5", cell_r),
         Paragraph("$282.20", cell_r)],
        [Paragraph("Subtotal", cell), "", "", Paragraph("$282.20", cell_r)],
        [Paragraph("VAT", cell), "", "",
         Paragraph("N/A (US-based)", cell_r)],
        [Paragraph("Total (Monthly)", cell_bw), "", "",
         Paragraph("$282.20", cell_rbw)],
    ]
    tbl = Table(data, colWidths=[88 * mm, 26 * mm, 16 * mm, 30 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BACKGROUND", (0, 2), (-1, 3), LIGHT),
        ("BACKGROUND", (0, 4), (-1, 4), NAVY),
        ("TEXTCOLOR", (0, 4), (-1, 4), colors.white),
        ("SPAN", (0, 2), (2, 2)),
        ("SPAN", (0, 3), (2, 3)),
        ("SPAN", (0, 4), (2, 4)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.white),
        ("GRID", (0, 1), (-1, 3), 0.4, colors.HexColor("#D6E2E6")),
    ]))
    # Recolor header total row text
    for r in (4,):
        tbl._argW  # noqa
    e.append(tbl)
    e.append(Spacer(1, 6))
    e.append(Paragraph(
        "Initial Term = 12 Months &nbsp;•&nbsp; Annual equivalent: "
        "<b>$3,386.40</b> (12 × $282.20).", small))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "Pricing is exempt from VAT as the customer is US-based. USD figures are "
        "converted from GBP (£42/seat) at an indicative rate of £1 = $1.3438 (4 Jun 2026); "
        "the rate at invoice/payment may vary.", small))

    e.append(Spacer(1, 14))
    e.append(HRFlowable(width="100%", thickness=1, color=LIGHT))
    e.append(Paragraph(
        '<a href="https://www.trainwithorca.com/terms-of-service" color="#5A6B78">'
        "Terms of Service</a> &nbsp;•&nbsp; Company Registration No. 17259799 "
        "&nbsp;•&nbsp; www.trainwithorca.com", small))

    doc.build(e)
    print("Built Royalty_Talent_ORCA_Proposal_USD.pdf")


if __name__ == "__main__":
    build()
