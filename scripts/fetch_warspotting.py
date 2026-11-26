#!/usr/bin/env python3
"""Download every Russian loss record from WarSpotting into one dated snapshot.

Writes data/raw/warspotting/russia_<YYYY-MM-DD>.csv.gz (one row per loss:
id, date, type, model, status). Run scripts/aggregate_losses.py afterwards to
rebuild losses_monthly.csv and matched_losses.csv from it.

Standard library only. Polite: one request at a time, 1 second apart, with
retries. A full run takes about 30-40 minutes.

    python scripts/fetch_warspotting.py                 # 2022-02-24 to yesterday
    python scripts/fetch_warspotting.py --start 2026-10-01 --end 2026-10-31

API used: https://ukr.warspotting.net/api/losses/russia/<date>/<page>/
(100 records per page). WarSpotting permits reuse "with appropriate credit".
"""
import argparse
import csv
import datetime as dt
import gzip
import json
import os
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data", "raw", "warspotting")
API = "https://ukr.warspotting.net/api/losses/russia/{date}/{page}/"
HEADERS = {"User-Agent": "burn-rate-index research script (open data project)"}
FIELDS = ["id", "date", "type", "model", "status"]
DELAY = 1.0


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                return {"losses": []}
            wait = DELAY * 2 ** (i + 1)
            print(f"  retry {i + 1} after {wait:.0f}s: {e}")
            time.sleep(wait)
    raise SystemExit(f"Giving up on {url}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", default="2022-02-24")
    p.add_argument("--end", default=(dt.date.today() - dt.timedelta(days=1)).isoformat())
    a = p.parse_args()
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    retrieved = dt.date.today().isoformat()

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"russia_{retrieved}.csv.gz")
    seen, n = set(), 0
    with gzip.open(out, "wt", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        day = start
        while day <= end:
            page = 1
            while True:
                data = get(API.format(date=day.isoformat(), page=page))
                rows = data.get("losses", [])
                for r in rows:
                    if r["id"] in seen:
                        continue
                    seen.add(r["id"])
                    w.writerow({k: r.get(k) for k in FIELDS})
                    n += 1
                time.sleep(DELAY)
                if len(rows) < 100:
                    break
                page += 1
            if day.day == 1:
                print(f"{day:%Y-%m}: {n:,} records so far", flush=True)
            day += dt.timedelta(days=1)
    print(f"Wrote {n:,} records to {out} (retrieved {retrieved})")


if __name__ == "__main__":
    main()
