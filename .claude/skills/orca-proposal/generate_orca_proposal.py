#!/usr/bin/env python3
"""
ORCA — AI Sales Coach proposal generator.

Renders the branded 6-page ORCA proposal PDF (Cover, The Gap, What's Included,
How It Works, Order Form, Fair Usage Policy) from a small JSON config that only
supplies the client + commercial details. Pages 2/3/4/6 are fixed product
content; only the Cover and Order Form change per client.

Usage:
    python generate_orca_proposal.py config.json output.pdf

Requires: pymupdf  (pip install pymupdf)

config.json fields (see config.example.json):
    contact, company, date            -> cover + order form
    headline_lines (optional list)    -> cover headline (defaults to brand line)
    line_desc, currency, unit_price,  -> order form line item
    qty, line_total
    subtotal, vat_label, vat, total_due  (vat_label/vat optional -> omit VAT row)
    term
    terms_url                         -> Terms of Service link (clickable)
"""
import sys, json
import fitz  # PyMuPDF

# ---- brand tokens -------------------------------------------------------
BG      = (0.039, 0.039, 0.039)   # #0a0a0a page background
CARD    = (0.086, 0.086, 0.086)   # #161616 panel
CARD2   = (0.105, 0.105, 0.105)   # slightly lighter panel
BORDER  = (0.16,  0.16,  0.16)    # subtle card border
BLUE    = (0.122, 0.635, 1.0)     # #1FA2FF accent
BLUE_D  = (0.04,  0.05,  0.07)    # dark text on blue bar
YELLOW  = (0.96,  0.77,  0.094)   # #F5C518 date / stats
WHITE   = (1, 1, 1)
GREY    = (0.70, 0.70, 0.70)      # body text
GREYM   = (0.55, 0.55, 0.55)
GREYD   = (0.42, 0.42, 0.42)      # footer

W, H = 595.0, 842.0               # A4 portrait
L, R = 49.0, 547.0                # text margins
CX0, CX1 = 47.0, 548.0            # card edges

HELV, BOLD, ITAL = "helv", "hebo", "hetit" if False else "heit"


def _t(page, x, y, s, font=HELV, size=10, color=WHITE):
    page.insert_text((x, y), s, fontname=font, fontsize=size, color=color)


def _box(page, rect, s, font=HELV, size=10, color=WHITE, align=0):
    return page.insert_textbox(fitz.Rect(rect), s, fontname=font,
                               fontsize=size, color=color, align=align)


def _rt(page, xright, y, s, font=HELV, size=10, color=WHITE):
    """Right-align single-line text at baseline y (reliable; no textbox padding)."""
    w = fitz.get_text_length(s, fontname=font, fontsize=size)
    page.insert_text((xright - w, y), s, fontname=font, fontsize=size, color=color)


def _ct(page, xc, y, s, font=HELV, size=10, color=WHITE):
    """Centre single-line text at baseline y."""
    w = fitz.get_text_length(s, fontname=font, fontsize=size)
    page.insert_text((xc - w / 2, y), s, fontname=font, fontsize=size, color=color)


def _card(page, x0, y0, x1, y1, fill=CARD, border=None, width=0.8):
    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=border, fill=fill,
                   width=width if border else 0)


def _bg(page):
    page.draw_rect(fitz.Rect(0, 0, W, H), color=None, fill=BG)


def _footer(page, section, n):
    _t(page, L, 816, "ORCA  ·  trainwithorca.com", HELV, 8, GREYD)
    _box(page, (W - 250, 808, R, 822), f"{section}  ·  {n} / 6",
         HELV, 8, GREYD, align=2)


def _label(page, s, y=92):
    _t(page, L, y, s, BOLD, 9.5, BLUE)


# ---- Page 1 : Cover -----------------------------------------------------
def page_cover(doc, cfg):
    p = doc.new_page(width=W, height=H); _bg(p)
    _t(p, L, 92, "ORCA", BOLD, 30, WHITE)
    p.draw_line(fitz.Point(L, 98), fitz.Point(L + 122, 98), color=BLUE, width=2.4)
    _t(p, L, 122, "AI Sales Coach for Recruiters", HELV, 11, GREY)

    p.draw_line(fitz.Point(L, 230), fitz.Point(L + 64, 230), color=BLUE, width=3)
    _t(p, L, 256, "PROPOSAL", BOLD, 10, BLUE)

    lines = cfg.get("headline_lines", ["Pick a call.", "Run it.", "Get better."])
    y = 322
    for ln in lines:
        _t(p, L - 2, y, ln, BOLD, 42, WHITE); y += 54
    _box(p, (L, y + 6, R, y + 70),
         cfg.get("subhead",
                 "Unlimited AI-driven call practice, instant scorecards, and a "
                 "voice debrief that replaces the call-replay sessions your "
                 "managers don't have time for."),
         HELV, 12.5, GREY)

    # prepared-for card
    cy0, cy1 = 574, 722
    _card(p, CX0, cy0, CX1, cy1, fill=CARD)
    p.draw_line(fitz.Point(CX0, cy0), fitz.Point(CX0, cy1), color=BLUE, width=2.5)
    _t(p, L + 17, cy0 + 30, "PREPARED FOR", BOLD, 9, BLUE)
    _t(p, L + 17, cy0 + 58, cfg["contact"], BOLD, 18, WHITE)
    _t(p, L + 17, cy0 + 80, cfg["company"], HELV, 13, GREY)
    _t(p, L + 17, cy0 + 116, "DATE", BOLD, 9, BLUE)
    _t(p, L + 17, cy0 + 134, cfg["date"].upper(), BOLD, 11, YELLOW)

    _footer(p, "Cover", 1)


# ---- Page 2 : The Gap ---------------------------------------------------
def page_gap(doc):
    p = doc.new_page(width=W, height=H); _bg(p)
    _label(p, "01  ·  THE GAP")
    _t(p, L - 2, 145, "Your top billers can't", BOLD, 33, WHITE)
    _t(p, L - 2, 188, "scale themselves.", BOLD, 33, WHITE)
    _box(p, (L, 248, R, 320),
         "Training content alone doesn't change behaviour. Managers don't have "
         "the bandwidth for consistent feedback. The methods your best recruiters "
         "use never make it into a playbook - and new starters take three months "
         "to ramp.", HELV, 12, GREY)

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
    y = 350
    for num, title, desc in items:
        _card(p, CX0, y, CX1, y + 78, fill=CARD)
        p.draw_line(fitz.Point(CX0, y), fitz.Point(CX0, y + 78), color=BLUE, width=2.5)
        _t(p, L + 17, y + 30, num, BOLD, 12, BLUE)
        _t(p, L + 48, y + 30, title, BOLD, 13, WHITE)
        _t(p, L + 48, y + 52, desc, HELV, 10.5, GREYM)
        y += 90
    _footer(p, "The Gap", 2)


# ---- Page 3 : What's Included ------------------------------------------
def page_included(doc):
    p = doc.new_page(width=W, height=H); _bg(p)
    _label(p, "02  ·  WHAT'S INCLUDED")

    hy0, hy1 = 215, 380
    _card(p, CX0, hy0, CX1, hy1, fill=CARD, border=BLUE, width=1.0)
    p.draw_rect(fitz.Rect(L + 14, hy0 + 26, L + 24, hy0 + 36), color=None, fill=YELLOW)
    _t(p, L + 32, hy0 + 35, "UNLIMITED ACCESS", BOLD, 9.5, YELLOW)
    _t(p, L + 14, hy0 + 72, "AI Call Coach", BOLD, 22, WHITE)
    _box(p, (L + 14, hy0 + 88, R - 8, hy1 - 12),
         "Live, voice-driven call practice with real-time objection handling and "
         "instant scoring. Every named user gets unlimited practice sessions, "
         "scorecards, and voice debriefs, subject to our Fair Usage Policy "
         "(page 6).", HELV, 11.5, GREY)

    cards = [
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
    gx, gy = CX0, 408
    cw = (CX1 - CX0 - 14) / 2
    ch = 112
    for i, (title, desc) in enumerate(cards):
        col, row = i % 2, i // 2
        x0 = gx + col * (cw + 14)
        y0 = gy + row * (ch + 14)
        _card(p, x0, y0, x0 + cw, y0 + ch, fill=CARD)
        p.draw_line(fitz.Point(x0 + 18, y0 + 26), fitz.Point(x0 + 40, y0 + 26),
                    color=BLUE, width=3)
        _t(p, x0 + 18, y0 + 56, title, BOLD, 13, WHITE)
        _box(p, (x0 + 18, y0 + 66, x0 + cw - 14, y0 + ch - 8), desc, HELV, 10, GREYM)
    _footer(p, "What's Included", 3)


# ---- Page 4 : How It Works ---------------------------------------------
def page_how(doc):
    p = doc.new_page(width=W, height=H); _bg(p)
    _label(p, "03  ·  HOW IT WORKS")
    steps = [
        ("01", "Choose",
         "Pick a scenario from 105+ real call types. Or upload a CV / LinkedIn URL "
         "to generate a custom one."),
        ("02", "Prepare",
         "Read the persona brief, company info, and likely objections before you dial."),
        ("03", "Practise",
         "Run the call live. The AI pushes back like a real prospect or candidate."),
        ("04", "Score",
         "Instant weighted scorecard with specific moments flagged and one clear action."),
        ("05", "Coach",
         "Orca Coach rings you back. Real voice conversation. Walks through what worked."),
    ]
    y = 150
    for num, title, desc in steps:
        _card(p, CX0, y, CX1, y + 80, fill=CARD)
        _t(p, L + 17, y + 30, num, BOLD, 13, BLUE)
        _t(p, L + 44, y + 30, title, BOLD, 13, BLUE)
        _box(p, (L + 17, y + 40, R - 12, y + 78), desc, HELV, 10.5, GREY)
        y += 90

    sy0, sy1 = y + 6, y + 92
    _card(p, CX0, sy0, CX1, sy1, fill=CARD)
    stats = [("105+", "Scenarios"), ("400+", "Lessons"), ("0", "Managers required")]
    seg = (CX1 - CX0) / 3
    for i, (big, lab) in enumerate(stats):
        cx = CX0 + seg * i + seg / 2
        _ct(p, cx, sy0 + 44, big, BOLD, 26, YELLOW)
        _ct(p, cx, sy0 + 68, lab, HELV, 10.5, GREY)
    _footer(p, "How It Works", 4)


# ---- Page 5 : Order Form -----------------------------------------------
def page_order(doc, cfg):
    p = doc.new_page(width=W, height=H); _bg(p)
    cur = cfg.get("currency", "")
    _label(p, "04  ·  ORDER FORM")
    _t(p, L - 2, 150, "Confirm the details below.", BOLD, 28, WHITE)

    PX, QX, TX = 372, 446, R - 6   # right edges: price / qty / total columns

    # client card
    cy0 = 210
    _card(p, CX0, cy0, CX1, cy0 + 70, fill=CARD)
    _t(p, L + 17, cy0 + 26, "CLIENT", BOLD, 9, BLUE)
    _t(p, L + 17, cy0 + 48, f"{cfg['contact']}  ·  {cfg['company']}", BOLD, 13, WHITE)
    _rt(p, R - 14, cy0 + 28, "DATE", BOLD, 9, BLUE)
    _rt(p, R - 14, cy0 + 50, cfg["date"].upper(), BOLD, 13, YELLOW)

    # table header
    ty = cy0 + 96
    _t(p, L + 12, ty, "DESCRIPTION", BOLD, 9, BLUE)
    _rt(p, PX, ty, "PRICE", BOLD, 9, BLUE)
    _rt(p, QX, ty, "QTY", BOLD, 9, BLUE)
    _rt(p, TX, ty, "TOTAL", BOLD, 9, BLUE)
    p.draw_line(fitz.Point(CX0, ty + 14), fitz.Point(CX1, ty + 14), color=BORDER, width=0.8)

    # line item
    ry = ty + 40
    _box(p, (L + 12, ry - 12, 300, ry + 28), cfg["line_desc"], HELV, 11, WHITE)
    _rt(p, PX, ry, f"{cur}{cfg['unit_price']}", HELV, 11, WHITE)
    _rt(p, QX, ry, str(cfg["qty"]), HELV, 11, WHITE)
    _rt(p, TX, ry, f"{cur}{cfg['line_total']}", HELV, 11, WHITE)
    p.draw_line(fitz.Point(CX0, ry + 34), fitz.Point(CX1, ry + 34), color=BORDER, width=0.8)

    yy = ry + 58
    # optional subtotal + VAT rows
    if cfg.get("vat"):
        _rt(p, QX, yy, "Subtotal", HELV, 10, GREY)
        _rt(p, TX, yy, f"{cur}{cfg['subtotal']}", HELV, 10, WHITE)
        yy += 20
        _rt(p, QX, yy, cfg.get("vat_label", "VAT (20%)"), HELV, 10, GREY)
        _rt(p, TX, yy, f"+{cur}{cfg['vat']}", HELV, 10, WHITE)
        yy += 28

    # TOTAL DUE bar
    by0 = yy
    p.draw_rect(fitz.Rect(330, by0, CX1, by0 + 46), color=None, fill=BLUE)
    _t(p, 348, by0 + 29, "TOTAL DUE", BOLD, 12, BLUE_D)
    _rt(p, CX1 - 16, by0 + 30, f"{cur}{cfg['total_due']}", BOLD, 15, BLUE_D)

    # term + signature card
    iy0 = by0 + 74
    _card(p, CX0, iy0, CX1, iy0 + 196, fill=CARD)
    _t(p, L + 17, iy0 + 28, "INITIAL TERM", BOLD, 9, BLUE)
    _t(p, L + 17, iy0 + 52, cfg["term"], BOLD, 16, WHITE)
    note = ("Includes unlimited AI Call Coach access for every named user, subject to "
            "our Fair Usage Policy (page 6) and our Terms of Service: "
            f"{cfg['terms_url']}")
    _box(p, (L + 17, iy0 + 62, R - 14, iy0 + 100), note, HELV, 9.5, GREYM)
    p.insert_link({"kind": fitz.LINK_URI, "from": fitz.Rect(L + 17, iy0 + 74, R - 14, iy0 + 100),
                   "uri": cfg["terms_url"]})

    _t(p, L + 17, iy0 + 128, "SIGNATURE", BOLD, 9, BLUE)
    p.draw_line(fitz.Point(L + 17, iy0 + 158), fitz.Point(290, iy0 + 158), color=GREYD, width=0.8)
    p.draw_line(fitz.Point(330, iy0 + 158), fitz.Point(R - 16, iy0 + 158), color=GREYD, width=0.8)
    _t(p, L + 17, iy0 + 152, cfg["contact"], ITAL, 12, WHITE)
    _t(p, L + 17, iy0 + 172, f"Signed on behalf of {cfg['company']}", HELV, 8.5, GREYD)
    _t(p, 338, iy0 + 172, "Date", HELV, 8.5, GREYD)
    _footer(p, "Order Form", 5)


# ---- Page 6 : Fair Usage Policy ----------------------------------------
def page_fair(doc, cfg):
    p = doc.new_page(width=W, height=H); _bg(p)
    _label(p, "05  ·  FAIR USAGE POLICY")
    _t(p, L - 2, 138, 'What "unlimited" means.', BOLD, 27, WHITE)
    _box(p, (L, 158, R, 206),
         "Every licensed user gets unlimited access to the AI Call Coach - practice "
         "sessions, scorecards, and voice debriefs. We don't impose a hard cap because "
         "we want your recruiters using the platform freely. This policy keeps the "
         "service fair and reliable for every customer.", HELV, 10, GREY)

    secs = [
        ("1. Expected usage",
         "ORCA is designed for active recruiter practice. Typical heavy use looks like "
         "3-8 full practice calls per user per working day, with associated scoring and "
         "debriefs. Some weeks will be busier than others - that is expected and entirely "
         "fine. Our infrastructure is sized for genuine human practice volume.", 80),
        ("2. Activity outside fair use",
         "(a) Account sharing. Each licensed seat is for one named recruiter; rotating a "
         "single login across an unlicensed team is not permitted - add seats instead "
         "(volume discounts apply). (b) Automated or non-human traffic - scripted use, bots "
         "or scrapers are not permitted. (c) Sustained extreme volume consistent with "
         "non-human generation (e.g. consistently exceeding 30 full calls per user per day "
         "over multiple weeks). (d) Resale or rebranding without written consent.", 98),
        ("3. How we handle a review",
         "If usage triggers a review: (i) we contact your billing/admin user by email with a "
         "clear summary; (ii) we give you 14 days to discuss, explain context, or adjust; "
         "(iii) if it continues and we cannot agree a resolution, we may rate-limit the "
         "affected user(s) or, in clear breach, suspend access pending resolution. We never "
         "silently cap, throttle or suspend without contacting you first.", 96),
        ("4. What this does not affect",
         "Genuine heavy use by a hard-working recruiter is welcome. Onboarding sprints, ramp "
         "programmes and bootcamp weeks where new starters practice intensively are explicitly "
         "fine. Power users running several calls per day over a sustained period are not in "
         "breach - that is the product working as intended.", 80),
        ("5. Changes to this policy",
         "We may update this Fair Usage Policy as the platform evolves. Material changes will "
         "be communicated to your billing contact at least 30 days before they take effect.", 58),
    ]
    y = 210
    for title, body, h in secs:
        _card(p, CX0, y, CX1, y + h, fill=CARD)
        p.draw_line(fitz.Point(CX0, y), fitz.Point(CX0, y + h), color=BLUE, width=2.2)
        _t(p, L + 15, y + 20, title, BOLD, 10.5, BLUE)
        _box(p, (L + 15, y + 23, R - 13, y + h - 4), body, HELV, 8.4, GREY)
        y += h + 9

    _t(p, L, y + 14, "Questions about this policy: charlotte@dohertygroup.io", HELV, 9, GREYM)
    _t(p, L, y + 32, f"Full Terms of Service: {cfg['terms_url']}", HELV, 9, BLUE)
    p.insert_link({"kind": fitz.LINK_URI, "from": fitz.Rect(L, y + 22, R, y + 36),
                   "uri": cfg["terms_url"]})
    _footer(p, "Fair Usage Policy", 6)


def build(cfg, out):
    cfg.setdefault("terms_url", "https://www.trainwithorca.com/terms-of-service")
    doc = fitz.open()
    page_cover(doc, cfg)
    page_gap(doc)
    page_included(doc)
    page_how(doc)
    page_order(doc, cfg)
    page_fair(doc, cfg)
    doc.save(out, deflate=True)
    doc.close()
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    with open(sys.argv[1]) as f:
        build(json.load(f), sys.argv[2])
