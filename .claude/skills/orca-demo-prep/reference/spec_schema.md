# Spec JSON schema

Pass a JSON file with these fields to `scripts/generate_orca_prep.py`.

| field             | type            | required | notes |
|-------------------|-----------------|----------|-------|
| `date`            | string          | no       | e.g. "3 Jun 2026". Defaults to today. |
| `company`         | string          | yes      | Prospect company name (large header). |
| `website`         | string          | no       | Shown under the name, e.g. "acme.com". |
| `contact_name`    | string          | yes      | Person you're meeting. |
| `contact_title`   | string          | yes      | Their role/title (wraps if long). |
| `linkedin`        | string          | no       | LinkedIn URL/handle (top-right of MEETING WITH). |
| `company_bullets` | string[]        | yes      | 4–6 factual lines about the company. |
| `prospect_bullets`| string[]        | yes      | 4–5 lines about the person & their remit. |
| `why_fits`        | {headline,body}[] | yes    | **Exactly 3**. Tailored fit reasons. |
| `open_with`       | string[]        | yes      | **4** opening / discovery questions. |
| `orca_url`        | string          | no       | Footer left. Defaults "trainwithorca.com". |
| `footer`          | string          | no       | Footer right. Defaults the "not for distribution" line. |

## Style rules
- ASCII only. Use " - " for dashes, straight quotes. No em dashes / smart quotes
  (the Helvetica base-14 font can't render them).
- Keep `company_bullets` / `prospect_bullets` to ~70 chars per line where you can
  (1–2 rendered lines each).
- `why_fits[].headline` = short bold claim; `body` = 3–5 short sentences.
- Make every line prospect-specific. Generic = failure.

See `harrington_starr_spec.json` for a complete worked example.
