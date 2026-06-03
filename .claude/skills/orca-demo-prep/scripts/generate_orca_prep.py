#!/usr/bin/env python3
"""
Generate an "ORCA DEMO PREP" one-page A4 PDF from a JSON spec.

Reproduces the ORCA brand template (dark background, blue + yellow accents,
Helvetica) used for the Brilliant Infotech demo-prep sheet. Layout flows
top-down and panels auto-size to their content, so bullets/questions of
varying length still render cleanly.

Usage:
    python3 generate_orca_prep.py spec.json [output.pdf]

If output.pdf is omitted, the file is written next to spec.json as
    ORCA_Demo_Prep__<Company>__<YYYYMMDD>.pdf

Requires: PyMuPDF  (pip install PyMuPDF)
"""

import json
import re
import sys
from datetime import datetime

import fitz  # PyMuPDF

# ---------------------------------------------------------------- brand colours
BG        = (0.039, 0.039, 0.039)   # near-black page background  #0A0A0A
PANEL     = (0.102, 0.102, 0.102)   # panel fill                  #1A1A1A
RULE      = (0.165, 0.165, 0.165)   # thin divider rules          #2A2A2A
BLUE      = (0.125, 0.671, 0.976)   # ORCA blue accent            #20ABF9
YELLOW    = (1.000, 0.961, 0.318)   # ORCA yellow accent          #FFF551
WHITE     = (1.000, 1.000, 1.000)
TEXT      = (0.965, 0.965, 0.953)   # off-white body text         #F6F6F3
MUTED     = (0.659, 0.659, 0.659)   # muted grey (date, linkedin) #A8A8A8
FOOTER_GR = (0.451, 0.451, 0.451)   # footer grey                 #737373

# fonts (PyMuPDF base-14 names)
F_REG  = "helv"
F_BOLD = "hebo"
F_ITAL = "heit"

# ------------------------------------------------------------------- page geom
PW, PH   = 595.276, 841.890         # A4 portrait, points
ML, MR   = 36.0, 559.276            # left / right content margins
COL_GAP  = 12.0                     # gap between the two top panels
PANEL_GAP = 12.0                    # vertical gap between stacked panels
PAD_X    = 14.0                     # panel inner left padding (36 -> 50)
LABEL_SZ = 7.5                      # section label size


def fits(text, font, size, width):
    """Greedy word-wrap; returns list of lines fitting within width."""
    words = text.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if fitz.get_text_length(trial, fontname=font, fontsize=size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


class Canvas:
    def __init__(self):
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=PW, height=PH)
        self.page.draw_rect(fitz.Rect(0, 0, PW, PH), color=None, fill=BG)

    def rect(self, x0, y0, x1, y1, fill):
        self.page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=None, fill=fill)

    def text(self, x, y, s, font, size, color, align_right=None):
        if align_right is not None:
            w = fitz.get_text_length(s, fontname=font, fontsize=size)
            x = align_right - w
        self.page.insert_text((x, y), s, fontname=font, fontsize=size, color=color)


def measure_bullets(bullets, width, size=8.5, lh=12.6):
    h = 0
    for b in bullets:
        n = len(fits(b, F_REG, size, width))
        h += max(28.0, n * lh + 6.0)
    return h


def draw_bullets(c, bullets, marker_x, text_x, top, width,
                 marker_color, size=8.5, lh=12.6):
    by = top
    for b in bullets:
        lines = fits(b, F_REG, size, width)
        # square marker aligned to first line cap height
        c.rect(marker_x, by - 6.0, marker_x + 3.0, by - 3.0, marker_color)
        for i, ln in enumerate(lines):
            c.text(text_x, by + i * lh, ln, F_REG, size, TEXT)
        by += max(28.0, len(lines) * lh + 6.0)
    return by


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: generate_orca_prep.py spec.json [output.pdf]")
    spec_path = sys.argv[1]
    with open(spec_path) as fh:
        s = json.load(fh)

    date_str = s.get("date") or datetime.now().strftime("%-d %b %Y")
    c = Canvas()

    # ---- header ----------------------------------------------------------
    c.text(ML, 44, "ORCA", F_BOLD, 14, WHITE)
    c.text(78, 44, "DEMO PREP", F_BOLD, 8, BLUE)
    c.text(0, 44, date_str, F_REG, 8.5, MUTED, align_right=MR)
    c.rect(ML, 52.0, MR, 52.6, RULE)

    # ---- company name + website -----------------------------------------
    c.text(ML, 92, s["company"], F_BOLD, 26, WHITE)
    if s.get("website"):
        c.text(ML, 108, s["website"], F_REG, 9.5, BLUE)

    y = 124.0

    # ---- MEETING WITH panel ---------------------------------------------
    title_lines = fits(s.get("contact_title", ""), F_REG, 9.5, MR - 50 - 14)
    mh = 14 + 14 + 18 + len(title_lines) * 12.6 + 8   # label,name gap, title
    mh = max(62.0, mh)
    c.rect(ML, y, MR, y + mh, PANEL)
    c.rect(ML, y, ML + 3, y + mh, YELLOW)            # yellow accent bar
    c.text(50, y + 14, "MEETING WITH", F_BOLD, LABEL_SZ, BLUE)
    if s.get("linkedin"):
        c.text(0, y + 14, s["linkedin"], F_REG, 8, MUTED, align_right=MR)
    c.text(50, y + 32, s.get("contact_name", ""), F_BOLD, 14, WHITE)
    ty = y + 50
    for ln in title_lines:
        c.text(50, ty, ln, F_REG, 9.5, TEXT)
        ty += 12.6
    y += mh + PANEL_GAP

    # ---- THE COMPANY / YOUR PROSPECT (side-by-side) ---------------------
    mid = ML + (MR - ML - COL_GAP) / 2            # 291.6-ish split
    lcol_text_w = mid - 8 - 58
    rcol_x0 = mid + COL_GAP
    rcol_text_x = rcol_x0 + 22                     # 325.6-ish
    rcol_text_w = MR - 8 - rcol_text_x

    comp = s.get("company_bullets", [])
    pros = s.get("prospect_bullets", [])
    label_to_bullets = 25.0                        # label baseline -> first bullet
    ph = label_to_bullets + max(measure_bullets(comp, lcol_text_w),
                                 measure_bullets(pros, rcol_text_w)) + 6
    c.rect(ML, y, mid, y + ph, PANEL)
    c.rect(rcol_x0, y, MR, y + ph, PANEL)
    c.text(50, y + 16, "THE COMPANY", F_BOLD, LABEL_SZ, BLUE)
    c.text(rcol_text_x, y + 16, "YOUR PROSPECT", F_BOLD, LABEL_SZ, BLUE)
    first_bullet = y + 16 + label_to_bullets
    draw_bullets(c, comp, 50, 58, first_bullet, lcol_text_w, BLUE)
    draw_bullets(c, pros, rcol_x0 + 14, rcol_text_x, first_bullet, rcol_text_w, YELLOW)
    y += ph + PANEL_GAP

    # ---- WHY ORCA FITS (3 columns) --------------------------------------
    fits_items = s.get("why_fits", [])[:3]
    col_w = (MR - ML - 2 * PAD_X) / 3              # three even columns
    body_w = col_w - 6
    # measure tallest column
    maxh = 0
    prepped = []
    for it in fits_items:
        hl = fits(it.get("headline", ""), F_BOLD, 10, body_w)
        bl = fits(it.get("body", ""), F_REG, 8.4, body_w)
        prepped.append((hl, bl))
        ch = 20 + len(hl) * 14.7 + 12 + len(bl) * 12.4
        maxh = max(maxh, ch)
    fh = 16 + 28 + maxh + 6                         # label + number + content
    c.rect(ML, y, MR, y + fh, PANEL)
    c.text(50, y + 16, "WHY ORCA FITS", F_BOLD, LABEL_SZ, BLUE)
    num_base = y + 50
    for i, (hl, bl) in enumerate(prepped):
        cx = 50 + i * col_w
        c.text(cx, num_base, str(i + 1), F_BOLD, 28, BLUE)
        hy = num_base + 20.7
        for ln in hl:
            c.text(cx, hy, ln, F_BOLD, 10, WHITE)
            hy += 14.7
        byy = hy + 11
        for ln in bl:
            c.text(cx, byy, ln, F_REG, 8.4, TEXT)
            byy += 12.4
    y += fh + PANEL_GAP

    # ---- OPEN WITH -------------------------------------------------------
    qs = s.get("open_with", [])
    q_text_w = MR - 12 - 62
    qh = 16 + 20
    q_lines = []
    for q in qs:
        ln = fits(q, F_ITAL, 9.5, q_text_w)
        q_lines.append(ln)
        qh += max(26.0, len(ln) * 12.6 + 13.4)
    c.rect(ML, y, MR, y + qh, PANEL)
    c.text(50, y + 16, "OPEN WITH", F_BOLD, LABEL_SZ, YELLOW)
    qy = y + 44
    for ln in q_lines:
        c.text(50, qy, '"', F_BOLD, 14, BLUE)
        for i, line in enumerate(ln):
            c.text(62, qy + 0.2 + i * 12.6, line, F_ITAL, 9.5, TEXT)
        qy += max(26.0, len(ln) * 12.6 + 13.4)

    # ---- footer ----------------------------------------------------------
    c.rect(ML, 799.9, MR, 800.5, RULE)
    c.text(ML, 809.9, s.get("orca_url", "trainwithorca.com"), F_BOLD, 8, BLUE)
    c.text(0, 809.9, s.get("footer", "Internal demo prep - not for distribution"),
           F_REG, 8, FOOTER_GR, align_right=MR)

    # ---- output ----------------------------------------------------------
    if len(sys.argv) >= 3:
        out = sys.argv[2]
    else:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", s["company"]).strip("_")
        stamp = datetime.now().strftime("%Y%m%d")
        out = f"ORCA_Demo_Prep__{slug}__{stamp}.pdf"
    c.doc.save(out)
    print(out)


if __name__ == "__main__":
    main()
