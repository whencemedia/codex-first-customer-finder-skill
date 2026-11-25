"""Append First Customer Finder prospects to the India tab of the Whence Lead Crawler sheet.

Reads a CSV whose header matches the India tab's columns, keeps rows with a public
email, skips anyone already in any lead tab (by website or email), and appends the rest.
"""
import csv
import json
import os
import re
import sys

INDIA_COLUMNS = ["Date added", "Segment", "Name", "Niche", "City", "Website", "Instagram",
                 "Founder Instagram", "Founder LinkedIn", "Size / budget signal",
                 "Brand-minded signal", "Public email", "Public phone", "Why they're a fit",
                 "Source", "Status", "Notes"]


def norm_site(url):
    url = re.sub(r"^https?://", "", (url or "").lower().strip())
    return re.sub(r"^www\.", "", url).split("/")[0]


def main(path, tab="India"):
    if not os.path.exists(path):
        print(f"No sheet rows file at {path}; nothing to add.")
        return
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    creds, sheet_id = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON"), os.environ.get("LEADS_SHEET_ID")
    if not (creds and sheet_id):
        print(f"{len(rows)} prospects found. Sheet secret not set, so they are only in the run's files.")
        return
    import gspread
    sh = gspread.service_account_from_dict(json.loads(creds)).open_by_key(sheet_id)

    sites, emails = set(), set()
    for t in ("Maps Leads", "India", "International", "Coaches"):
        try:
            data = sh.worksheet(t).get_all_values()
        except Exception:
            continue
        if not data:
            continue
        head = [h.lower() for h in data[0]]
        for r in data[1:]:
            for k, v in zip(head, r):
                if "website" in k and v:
                    sites.add(norm_site(v))
                if "email" in k and "@" in v:
                    emails.add(v.strip().lower())

    new = []
    for r in rows:
        email = (r.get("Public email") or "").strip().lower()
        site = norm_site(r.get("Website"))
        if "@" not in email or email in emails or (site and site in sites):
            continue
        emails.add(email)
        if site:
            sites.add(site)
        r["Status"] = r.get("Status") or "New"
        r["Notes"] = ("Found by First Customer Finder on GitHub. " + (r.get("Notes") or "")).strip()
        new.append([str(r.get(c, "") or "") for c in INDIA_COLUMNS])

    if new:
        sh.worksheet(tab).append_rows(new, value_input_option="RAW", table_range="A1")
    print(f"Added {len(new)} new prospects to the {tab} tab")
    for n in new:
        print(f" - {n[2]} ({n[4]}): {n[11]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "India")
