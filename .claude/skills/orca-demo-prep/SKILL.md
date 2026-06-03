---
name: orca-demo-prep
description: >
  Create an "ORCA DEMO PREP" one-page sales/demo prep sheet (branded PDF) for a
  prospect meeting. Use when the user asks to prep for a meeting/demo/sales call,
  build a prospect brief, or "do an ORCA prep doc" for a named company. Researches
  the prospect company and the meeting contact, then renders the branded one-pager.
  ORCA = Online Recruitment Coaching Academy (trainwithorca.com); the prospect is
  always the company ORCA is selling into.
---

# ORCA Demo Prep

Produces a single-page A4 PDF in ORCA's brand style: dark background with blue
(#20ABF9) and yellow (#FFF551) accents, Helvetica. The sheet briefs an ORCA rep
before a demo/sales meeting. It has five sections: header, MEETING WITH,
THE COMPANY + YOUR PROSPECT (side-by-side), WHY ORCA FITS (3 reasons), and
OPEN WITH (4 discovery questions).

## What ORCA is (use this to keep "WHY ORCA FITS" accurate)

ORCA — **Online Recruitment Coaching Academy** (trainwithorca.com) — is a global
recruitment **training platform**. Keep these facts straight; do not invent
features:

- Weekly **live / as-live streamed coaching** plus **on-demand courses** and
  ready-to-use **toolkits, scripts and frameworks**.
- Monthly themes over ~4 weeks (e.g. business development, advanced headhunting,
  growth mindset); recruiters watch lessons and complete assessments.
- Taught by **agency founders, leadership coaches, performance experts and
  recruitment trainers**.
- **Scales from a solo recruiter to 60+ person teams** — consistent standard
  across desks/offices.
- Core value: every recruiter — graduate to senior — gets repeatable, consistent,
  world-class development without flying trainers around or burning the leadership
  team's time delivering sessions.

`reference/orca_facts.md` has the full briefing. Read it before writing "WHY ORCA FITS".

## Inputs you need

1. **Prospect company** — name + website.
2. **Meeting contact** — name, job title, and LinkedIn URL.

If the user hasn't given the contact, ask who the meeting is with (one short
question). If they don't know yet, pick the most senior plausible buyer
(Founder/CEO, MD, or Head of L&D / Talent / People) and clearly note the
assumption in your reply so they can swap it.

## Workflow

1. **Research the prospect.** Use WebSearch (and WebFetch where allowed; many
   corporate sites return 403 to WebFetch — fall back to WebSearch). Gather:
   what the company does, sector, size, offices/locations, year founded, group
   structure/brands, notable clients, awards, and especially any **training /
   L&D / academy / recruiter-development** signals (these power the fit story).
   Then research the **contact**: role, seniority, tenure, background, public
   presence (podcasts, articles), and whether they likely own or influence the
   training/enablement budget.

2. **Write the spec JSON** (see `reference/spec_schema.md` and
   `reference/harrington_starr_spec.json` for a worked example). Rules:
   - `company_bullets`: 4–6 punchy, factual lines about the company. Keep each
     to ~1 line (≤ ~70 chars renders on one line; 2 lines is fine).
     Use " - " (spaced hyphen), not em dashes or non-ASCII.
   - `prospect_bullets`: 4–5 lines about the specific person and why they matter
     to the sale (remit, budget influence, what they care about).
   - `why_fits`: **exactly 3** objects, each `{headline, body}`. Tailor every one
     to THIS prospect using real facts you found, mapped to ORCA's real
     capabilities above. The headline is a short bold claim; the body is 3–5
     short sentences. Lead with their strongest fit signal.
   - `open_with`: **4** discovery/opening questions that reference specifics you
     found (their training award, their growth, their multi-office setup, the
     top-biller vs average-biller gap, etc.). Keep them conversational.
   - Use plain ASCII punctuation throughout (Helvetica base-14 has no smart
     quotes/em dashes). Use " - " for dashes and straight quotes.
   - `date` defaults to today if omitted.

3. **Generate the PDF:**
   ```bash
   python3 .claude/skills/orca-demo-prep/scripts/generate_orca_prep.py <spec.json> [output.pdf]
   ```
   The script needs PyMuPDF (`pip install PyMuPDF` if missing — it also needs a
   working `cffi`; if import fails run `pip install --force-reinstall cffi`).
   With no output path it writes `ORCA_Demo_Prep__<Company>__<YYYYMMDD>.pdf` in
   the current directory.

4. **Verify, then deliver.** Render page 1 to a PNG and eyeball it
   (`fitz.open(pdf)[0].get_pixmap(dpi=130).save('preview.png')`, then Read the
   image) to confirm nothing overflows the page. Send the finished PDF to the
   user with `SendUserFile`.

## Notes

- The output is internal prep ("Internal demo prep - not for distribution"
  footer) — it is not sent to the prospect.
- Panels auto-size to content, so longer bullets/questions still fit, but keep
  lines tight: this is a glanceable one-pager, not a report.
- Keep the tone sharp and specific. Generic bullets ("a great company") are
  failures — every line should be something you could only say about this
  prospect.
