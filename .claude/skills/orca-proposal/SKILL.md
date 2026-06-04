---
name: orca-proposal
description: >
  Generate a branded ORCA "AI Sales Coach for Recruiters" client proposal as a
  polished 6-page PDF (Cover, The Gap, What's Included, How It Works, Order Form,
  Fair Usage Policy). Use whenever someone asks for an "ORCA proposal" for a named
  client/company with seats and pricing. Pages 2/3/4/6 are fixed product content;
  only the Cover and Order Form change per client. Includes the ORCA Terms of
  Service link and company registration number.
---

# ORCA Proposal Skill

Produces the standard ORCA AI Sales Coach proposal PDF, matching the house design
(dark theme, blue `#1FA2FF` + yellow `#F5C518` accents, white headlines).

## How to use

1. Make sure `pymupdf` is installed: `pip install pymupdf`
2. Create a client config JSON (copy `config.example.json`, drop it in `clients/`).
3. Run:
   ```bash
   python generate_orca_proposal.py clients/<client>.json "<Client> - ORCA Proposal.pdf"
   ```
4. To preview, rasterise pages with PyMuPDF (`page.get_pixmap(dpi=110)`).

## Config fields (`clients/*.json`)

| Field            | Notes                                                                 |
|------------------|-----------------------------------------------------------------------|
| `contact`        | Client contact name (Cover + Order Form).                             |
| `company`        | Client company name.                                                  |
| `date`           | Proposal date, e.g. `"4 June 2026"`.                                  |
| `headline_lines` | Optional list; defaults to `["Pick a call.","Run it.","Get better."]`.|
| `subhead`        | Optional cover sub-line; sensible default provided.                  |
| `line_desc`      | Order-form line item description.                                     |
| `currency`       | Symbol, e.g. `"£"` or `"$"`.                                          |
| `unit_price`     | Per-user price (string, no symbol), e.g. `"42"`.                      |
| `qty`            | Number of user licences/seats.                                        |
| `line_total`     | `unit_price x qty`, e.g. `"252.00"`.                                  |
| `subtotal`/`vat`/`vat_label` | Optional. Include `vat` to show a VAT row + subtotal. Omit `vat` for a flat total (matches USD examples with no VAT). |
| `total_due`      | Final amount shown in the blue TOTAL DUE bar.                         |
| `term`           | Initial term, e.g. `"12 months"`.                                    |
| `terms_url`      | Terms of Service URL. Defaults to `https://www.trainwithorca.com/terms-of-service`. |

## Standing details (baked in)

- Terms of Service: **https://www.trainwithorca.com/terms-of-service** (clickable on
  the Order Form and Fair Usage Policy pages).
- Company Registration No. **17259799**.
- Policy contact: charlotte@dohertygroup.io.

## Pricing notes

- For UK £ deals, ORCA prices are quoted **ex-VAT**: set `line_total`/`subtotal`,
  add `vat` (20%) and set `total_due` to the VAT-inclusive figure.
- For non-VAT/USD deals, omit `vat` and set `total_due` to `line_total`.

## Editing the fixed pages

Product copy for The Gap / What's Included / How It Works / Fair Usage Policy lives
directly in `generate_orca_proposal.py` (functions `page_gap`, `page_included`,
`page_how`, `page_fair`). Card heights on the Fair Usage page must comfortably
exceed the wrapped text — PyMuPDF `insert_textbox` renders **nothing** if the text
overflows the box, so give it headroom and re-preview after edits.
