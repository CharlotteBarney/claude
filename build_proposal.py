#!/usr/bin/env python3
"""Royalty Talent - ORCA Proposal in the saved ORCA deck format (dark theme, 6 pages).

Order Form (page 5) is priced in USD with VAT removed (US-based customer).
Basis: $56.44/seat x 5 = $282.20/mo  (GBP42/seat @ GBP1 = USD1.3438, 4 Jun 2026).
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

W, H = A4  # 595 x 842
LM = 52
RM = W - 52
CW = RM - LM  # content width

# Palette
BG      = colors.HexColor("#0B0B0D")
CARD    = colors.HexColor("#17181C")
CARD2   = colors.HexColor("#1B1C21")
BLUE    = colors.HexColor("#3B82F6")
BLUEDK  = colors.HexColor("#2F6FE0")
WHITE   = colors.HexColor("#FFFFFF")
OFFW    = colors.HexColor("#F2F3F5")
MUTE    = colors.HexColor("#9AA1A9")
MUTE2   = colors.HexColor("#6B7178")
DIM     = colors.HexColor("#565C63")
AMBER   = colors.HexColor("#F5C518")
ONBLUE  = colors.HexColor("#0A1A2F")

REG, BOLD, ITAL = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def ty(t):
    return H - t


def bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def footer(c, section, page):
    c.setFont(REG, 8)
    c.setFillColor(MUTE2)
    c.drawString(LM, 30, "ORCA  ·  trainwithorca.com")
    c.drawRightString(RM, 30, f"{section} · {page} / 6")


def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, x, top, text, font, size, maxw, color, leading=None):
    leading = leading or size * 1.42
    c.setFont(font, size)
    c.setFillColor(color)
    y = ty(top)
    for ln in wrap(c, text, font, size, maxw):
        c.drawString(x, y, ln)
        y -= leading
    return H - y  # bottom as top-coord


def caps(c, x, top, text, color, size=9, tracking=1.4, right=False):
    c.setFont(BOLD, size)
    c.setFillColor(color)
    total = sum(c.stringWidth(ch, BOLD, size) + tracking for ch in text) - tracking
    sx = x - total if right else x
    y = ty(top)
    for ch in text:
        c.drawString(sx, y, ch)
        sx += c.stringWidth(ch, BOLD, size) + tracking


def tick(c, x, top, w=44, h=3, color=BLUE):
    c.setFillColor(color)
    c.rect(x, ty(top) - h, w, h, fill=1, stroke=0)


def card(c, x, top, w, h, fill=CARD, left=None, border=None):
    c.setFillColor(fill)
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(1.4)
        c.roundRect(x, ty(top) - h, w, h, 6, fill=1, stroke=1)
    else:
        c.roundRect(x, ty(top) - h, w, h, 5, fill=1, stroke=0)
    if left:
        c.setFillColor(left)
        c.roundRect(x, ty(top) - h, 4, h, 1.5, fill=1, stroke=0)


# ---------------------------------------------------------------- PAGE 1 COVER
def page_cover(c):
    bg(c)
    c.setFont(BOLD, 36)
    c.setFillColor(WHITE)
    c.drawString(LM, ty(132), "ORCA")
    wd = c.stringWidth("ORCA", BOLD, 36)
    c.setFillColor(BLUE)
    c.rect(LM, ty(146), wd + 8, 3.5, fill=1, stroke=0)
    c.setFont(REG, 12)
    c.setFillColor(MUTE)
    c.drawString(LM, ty(170), "AI Sales Coach for Recruiters")

    tick(c, LM, 350)
    caps(c, LM, 392, "PROPOSAL", BLUE, 10, 2)

    c.setFillColor(WHITE)
    c.setFont(BOLD, 42)
    for i, line in enumerate(["Pick a call.", "Run it.", "Get better."]):
        c.drawString(LM, ty(458 + i * 52), line)

    para(c, LM, 600,
         "Unlimited AI-driven call practice, instant scorecards, and a voice "
         "debrief that replaces the call-replay sessions your managers don't "
         "have time for.", REG, 12.5, CW, MUTE, 19)

    # client / date card
    ct = 632
    ch = 150
    card(c, LM, ct, CW, ch, fill=CARD, left=BLUE)
    caps(c, LM + 26, ct + 36, "PREPARED FOR", BLUE, 9, 1.4)
    c.setFont(BOLD, 17)
    c.setFillColor(WHITE)
    c.drawString(LM + 26, ty(ct + 64), "Ivan Duschatzky")
    c.setFont(REG, 12.5)
    c.setFillColor(MUTE)
    c.drawString(LM + 26, ty(ct + 86), "Royalty Talent")
    caps(c, LM + 26, ct + 118, "DATE", BLUE, 9, 1.4)
    c.setFont(BOLD, 13)
    c.setFillColor(AMBER)
    c.drawString(LM + 26, ty(ct + 140), "4 JUNE 2026")

    footer(c, "Cover", 1)
    c.showPage()


# ------------------------------------------------------------------ PAGE 2 GAP
def page_gap(c):
    bg(c)
    caps(c, LM, 96, "01  ·  THE GAP", BLUE, 9.5, 1.5)
    c.setFont(BOLD, 30)
    c.setFillColor(WHITE)
    c.drawString(LM, ty(150), "Your top billers can't")
    c.drawString(LM, ty(186), "scale themselves.")
    para(c, LM, 244,
         "Training content alone doesn't change behaviour. Managers don't have "
         "the bandwidth for consistent feedback. The methods your best "
         "recruiters use never make it into a playbook - and new starters take "
         "three months to ramp.", REG, 12, CW, MUTE, 18)

    items = [
        ("01", "Training without practice",
         "Recruiters watch, nod, and do exactly what they did yesterday."),
        ("02", "Feedback is a luxury",
         "Managers can't sit through 45-minute call replays five times a week."),
        ("03", "Top biller methods walk out the door",
         "When star recruiters leave, their playbook leaves with them."),
        ("04", "Ramp time eats your margin",
         "Three months to productivity is too slow when desks need to bill."),
    ]
    top, h, pitch = 360, 80, 95
    for i, (n, t, d) in enumerate(items):
        y0 = top + i * pitch
        card(c, LM, y0, CW, h, fill=CARD, left=BLUE)
        c.setFont(BOLD, 13)
        c.setFillColor(BLUE)
        c.drawString(LM + 28, ty(y0 + 30), n)
        c.setFont(BOLD, 13)
        c.setFillColor(WHITE)
        c.drawString(LM + 62, ty(y0 + 30), t)
        para(c, LM + 62, y0 + 50, d, REG, 11, CW - 90, MUTE, 14)

    footer(c, "The Gap", 2)
    c.showPage()


# -------------------------------------------------------- PAGE 3 WHATS INCLUDED
def page_included(c):
    bg(c)
    caps(c, LM, 96, "02  ·  WHAT'S INCLUDED", BLUE, 9.5, 1.5)

    bt, bh = 200, 150
    card(c, LM, bt, CW, bh, fill=CARD2, border=BLUE)
    c.setFillColor(AMBER)
    c.rect(LM + 26, ty(bt + 38) - 2, 11, 11, fill=1, stroke=0)
    caps(c, LM + 46, bt + 36, "UNLIMITED ACCESS", BLUE, 9, 1.4)
    c.setFont(BOLD, 23)
    c.setFillColor(WHITE)
    c.drawString(LM + 26, ty(bt + 70), "AI Call Coach")
    para(c, LM + 26, bt + 94,
         "Live, voice-driven call practice with real-time objection handling "
         "and instant scoring. Every named user gets unlimited practice "
         "sessions, scorecards, and voice debriefs, subject to our Fair Usage "
         "Policy (page 6).", REG, 11.5, CW - 52, MUTE, 16)

    feats = [
        ("105+ Practice Scenarios",
         "Cold calls, qualification, closing, counter-offers - client and candidate side."),
        ("400+ On-Demand Lessons",
         "Built by active practitioners, not career trainers."),
        ("Instant Scorecard",
         "Weighted criteria, written coaching notes, flagged call moments."),
        ("Voice Debrief",
         "Orca Coach rings the recruiter back to talk the call through."),
        ("Manager Dashboard",
         "Assign scenarios, track progress, auto-scored calls. No replay sessions."),
        ("Live Coaching Sessions",
         "Twice-weekly expert sessions with Dan Alexander and rotating trainers."),
    ]
    colw = (CW - 16) / 2
    rx = [LM, LM + colw + 16]
    gtop, ch, rpitch = 400, 96, 108
    for i, (t, d) in enumerate(feats):
        x = rx[i % 2]
        y0 = gtop + (i // 2) * rpitch
        card(c, x, y0, colw, ch, fill=CARD)
        tick(c, x + 22, y0 + 24, 26, 3)
        c.setFont(BOLD, 13)
        c.setFillColor(WHITE)
        c.drawString(x + 22, ty(y0 + 52), t)
        para(c, x + 22, y0 + 70, d, REG, 10.5, colw - 44, MUTE, 14)

    footer(c, "What's Included", 3)
    c.showPage()


# ------------------------------------------------------------ PAGE 4 HOW IT WORKS
def page_how(c):
    bg(c)
    caps(c, LM, 96, "03  ·  HOW IT WORKS", BLUE, 9.5, 1.5)

    steps = [
        ("01", "Choose",
         "Pick a scenario from 105+ real call types. Or upload a CV / LinkedIn URL to generate a custom one."),
        ("02", "Prepare",
         "Read the persona brief, company info, and likely objections before you dial."),
        ("03", "Practise",
         "Run the call live. The AI pushes back like a real prospect or candidate."),
        ("04", "Score",
         "Instant weighted scorecard with specific moments flagged and one clear action."),
        ("05", "Coach",
         "Orca Coach rings you back. Real voice conversation. Walks through what worked."),
    ]
    top, h, pitch = 150, 74, 88
    for i, (n, t, d) in enumerate(steps):
        y0 = top + i * pitch
        card(c, LM, y0, CW, h, fill=CARD)
        c.setFont(BOLD, 13)
        c.setFillColor(BLUE)
        c.drawString(LM + 24, ty(y0 + 30), n)
        c.setFont(BOLD, 13)
        c.setFillColor(WHITE)
        c.drawString(LM + 50, ty(y0 + 30), t)
        para(c, LM + 24, y0 + 50, d, REG, 11, CW - 48, MUTE, 14)

    # stat band
    st, sh = 615, 110
    card(c, LM, st, CW, sh, fill=CARD2)
    stats = [("105+", "Scenarios"), ("400+", "Lessons"), ("0", "Managers required")]
    third = CW / 3
    for i, (num, lab) in enumerate(stats):
        cx = LM + third * i + third / 2
        c.setFont(BOLD, 34)
        c.setFillColor(AMBER)
        c.drawCentredString(cx, ty(st + 56), num)
        c.setFont(REG, 11.5)
        c.setFillColor(MUTE)
        c.drawCentredString(cx, ty(st + 82), lab)

    footer(c, "How It Works", 4)
    c.showPage()


# -------------------------------------------------------- PAGE 5 ORDER FORM (USD)
def page_order(c):
    bg(c)
    caps(c, LM, 96, "04  ·  ORDER FORM", BLUE, 9.5, 1.5)
    c.setFont(BOLD, 30)
    c.setFillColor(WHITE)
    c.drawString(LM, ty(156), "Confirm the details below.")

    # client/date card
    ct, ch = 210, 76
    card(c, LM, ct, CW, ch, fill=CARD)
    caps(c, LM + 26, ct + 30, "CLIENT", BLUE, 9, 1.4)
    c.setFont(BOLD, 15)
    c.setFillColor(WHITE)
    c.drawString(LM + 26, ct_y := ty(ct + 56), "Ivan Duschatzky  ·  Royalty Talent")
    caps(c, RM - 26, ct + 30, "DATE", BLUE, 9, 1.4, right=True)
    c.setFont(BOLD, 14)
    c.setFillColor(AMBER)
    c.drawRightString(RM - 26, ty(ct + 56), "4 JUNE 2026")

    # table columns (right edges)
    x_desc = LM + 6
    x_price = LM + 348
    x_qty = LM + 412
    x_total = RM - 6

    th = 322
    caps(c, x_desc, th, "DESCRIPTION", BLUE, 9, 1)
    caps(c, x_price, th, "PRICE", BLUE, 9, 1, right=True)
    caps(c, x_qty, th, "QTY", BLUE, 9, 1, right=True)
    caps(c, x_total, th, "TOTAL", BLUE, 9, 1, right=True)
    c.setStrokeColor(colors.HexColor("#2A2C31"))
    c.setLineWidth(0.8)
    c.line(LM, ty(th + 12), RM, ty(th + 12))

    # line item
    rt = th + 40
    c.setFont(REG, 12)
    c.setFillColor(OFFW)
    c.drawString(x_desc, ty(rt), "ORCA - Unlimited AI Call Coach access per user")
    c.setFillColor(MUTE)
    c.setFont(REG, 11)
    c.drawString(x_desc, ty(rt + 18), "(fair usage applies)")
    c.setFont(REG, 12)
    c.setFillColor(OFFW)
    c.drawRightString(x_price, ty(rt), "$56.44")
    c.drawRightString(x_qty, ty(rt), "5")
    c.drawRightString(x_total, ty(rt), "$282.20")
    c.setStrokeColor(colors.HexColor("#2A2C31"))
    c.line(LM, ty(rt + 36), RM, ty(rt + 36))

    # subtotal / vat
    sy = rt + 62
    c.setFont(REG, 11.5)
    c.setFillColor(MUTE)
    c.drawRightString(x_price, ty(sy), "Subtotal")
    c.setFillColor(OFFW)
    c.drawRightString(x_total, ty(sy), "$282.20")
    c.setFillColor(MUTE)
    c.drawRightString(x_price, ty(sy + 22), "VAT")
    c.setFillColor(OFFW)
    c.drawRightString(x_total, ty(sy + 22), "Exempt (US-based)")

    # total due band
    bt, bw, bh = sy + 48, 250, 50
    bx = RM - bw
    c.setFillColor(BLUE)
    c.roundRect(bx, ty(bt) - bh, bw, bh, 5, fill=1, stroke=0)
    caps(c, bx + 22, bt + 31, "TOTAL DUE", ONBLUE, 11, 1)
    c.setFont(BOLD, 19)
    c.setFillColor(ONBLUE)
    c.drawRightString(bx + bw - 20, ty(bt + 33), "$282.20")

    # initial term + signature card
    it, ih = bt + bh + 20, 168
    card(c, LM, it, CW, ih, fill=CARD)
    caps(c, LM + 26, it + 30, "INITIAL TERM", BLUE, 9, 1.4)
    c.setFont(BOLD, 18)
    c.setFillColor(WHITE)
    c.drawString(LM + 26, ty(it + 56), "12 months")
    para(c, LM + 26, it + 76,
         "Includes unlimited AI Call Coach access for every named user, subject "
         "to our Fair Usage Policy (page 6) and our Terms of Service: "
         "https://www.trainwithorca.com/terms-of-service", REG, 9.5, CW - 52, MUTE, 13)
    caps(c, LM + 26, it + 122, "SIGNATURE", BLUE, 9, 1.4)
    c.setFont(ITAL, 13)
    c.setFillColor(OFFW)
    c.drawString(LM + 26, ty(it + 142), "Ivan Duschatzky")
    c.setStrokeColor(DIM)
    c.setLineWidth(0.7)
    c.line(LM + 26, ty(it + 146), LM + 250, ty(it + 146))
    c.line(LM + 290, ty(it + 146), RM - 26, ty(it + 146))
    c.setFont(REG, 9)
    c.setFillColor(MUTE2)
    c.drawString(LM + 26, ty(it + 158), "Signed on behalf of Royalty Talent")
    c.drawString(LM + 290, ty(it + 158), "Date")

    # conversion note
    para(c, LM, it + ih + 22,
         "Pricing is exempt from VAT as the customer is US-based. USD figures "
         "are converted from GBP (£42/seat) at an indicative rate of "
         "£1 = $1.3438 (4 Jun 2026); the rate at invoice may vary. Annual "
         "equivalent: $3,386.40 (12 × $282.20).", REG, 8.5, CW, MUTE2, 12)

    footer(c, "Order Form", 5)
    c.showPage()


# --------------------------------------------------------- PAGE 6 FAIR USAGE
def policy_item(c, top, title, body):
    lines = wrap(c, body, REG, 8.3, CW - 36)
    h = 26 + len(lines) * 10.5 + 12
    card(c, LM, top, CW, h, fill=CARD)
    c.setFont(BOLD, 10)
    c.setFillColor(BLUE)
    c.drawString(LM + 18, ty(top + 22), title)
    y = ty(top + 38)
    c.setFont(REG, 8.3)
    c.setFillColor(MUTE)
    for ln in lines:
        c.drawString(LM + 18, y, ln)
        y -= 10.5
    return top + h + 10


def page_policy(c):
    bg(c)
    caps(c, LM, 74, "05  ·  FAIR USAGE POLICY", BLUE, 9.5, 1.5)
    c.setFont(BOLD, 26)
    c.setFillColor(WHITE)
    c.drawString(LM, ty(116), "What “unlimited” means.")
    nxt = para(c, LM, 150,
               "Every licensed user gets unlimited access to the AI Call Coach - "
               "practice sessions, scorecards, and voice debriefs. We don't impose "
               "a hard cap because we want your recruiters using the platform "
               "freely. This policy keeps the service fair and reliable for every "
               "customer.", REG, 10.5, CW, MUTE, 15)

    items = [
        ("1.  Expected usage",
         "ORCA is designed for active recruiter practice. Typical heavy use looks like 3-8 full practice calls per "
         "user per working day, with associated scoring and debriefs. Some weeks will be busier than others - that "
         "is expected and entirely fine. Our infrastructure is sized for genuine human practice volume."),
        ("2.  Activity outside fair use",
         "(a) Account sharing. Each licensed seat is for one named recruiter; rotating a single login across an "
         "unlicensed team is not permitted - add seats instead (volume discounts apply). (b) Automated or "
         "non-human traffic - scripted use, bots or scrapers are not permitted. (c) Sustained extreme volume "
         "consistent with non-human generation (e.g. consistently exceeding 30 full calls per user per day over "
         "multiple weeks). (d) Resale or rebranding without written consent."),
        ("3.  How we handle a review",
         "If usage triggers a review: (i) we contact your billing/admin user by email with a clear summary; (ii) we "
         "give you 14 days to discuss, explain context, or adjust; (iii) if it continues and we cannot agree a "
         "resolution, we may rate-limit the affected user(s) or, in clear breach, suspend access pending "
         "resolution. We never silently cap, throttle or suspend without contacting you first."),
        ("4.  What this does not affect",
         "Genuine heavy use by a hard-working recruiter is welcome. Onboarding sprints, ramp programmes and "
         "bootcamp weeks where new starters practice intensively are explicitly fine. Power users running several "
         "calls per day over a sustained period are not in breach - that is the product working as intended."),
        ("5.  Changes to this policy",
         "We may update this Fair Usage Policy as the platform evolves. Material changes will be communicated to "
         "your billing contact at least 30 days before they take effect."),
    ]
    top = nxt + 14
    for t, b in items:
        top = policy_item(c, top, t, b)

    top += 4
    c.setFont(REG, 8.5)
    c.setFillColor(MUTE)
    c.drawString(LM, ty(top + 6), "Questions about this policy: charlotte@dohertygroup.io")
    c.drawString(LM, ty(top + 22),
                 "Full Terms of Service: https://www.trainwithorca.com/terms-of-service")

    footer(c, "Fair Usage Policy", 6)
    c.showPage()


def build():
    c = canvas.Canvas("Royalty_Talent_ORCA_Proposal_USD.pdf", pagesize=A4)
    c.setTitle("Royalty Talent - ORCA Proposal")
    c.setAuthor("ORCA")
    page_cover(c)
    page_gap(c)
    page_included(c)
    page_how(c)
    page_order(c)
    page_policy(c)
    c.save()
    print("Built Royalty_Talent_ORCA_Proposal_USD.pdf")


if __name__ == "__main__":
    build()
