#!/usr/bin/env python3
"""Rebuild losses_monthly.csv and matched_losses.csv from a WarSpotting snapshot.

    python scripts/aggregate_losses.py [data/raw/warspotting/russia_<date>.csv.gz]

Uses the newest snapshot by default. Counts destroyed, captured and abandoned
equipment (not damaged), as in the first version.

  losses_monthly.csv   losses per month in eight categories (CATEGORY below)
  matched_losses.csv   losses per year of the 14 platform types GUR has torn
                       down (MATCH below), counted up to the end of the latest
                       month in launches.csv, so both sides of the headline
                       comparison cover the same months. The per-unit record
                       columns are copied from unit_profiles.csv.

Prints WarSpotting models that look like a matched platform but are not
matched, so new variants can be reviewed by hand. Standard library only.
"""
import collections
import csv
import gzip
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
SNAP = os.path.join(RAW, "warspotting")
COUNTED = {"Destroyed", "Captured", "Abandoned"}

CATEGORY = {
    "Tanks": "Tanks",
    "Infantry fighting vehicles": "Armoured vehicles",
    "Infantry mobility vehicles": "Armoured vehicles",
    "Towed artillery": "Artillery",
    "Self-propelled artillery": "Artillery",
    "Rocket and missile artillery": "Artillery",
    "Anti-aircraft systems": "Air defence",
    "Radars, jammers": "Air defence",
    "Airplanes": "Aircraft",
    "Helicopters": "Aircraft",
    "Drones": "Drones",
    "Transport": "Transport",
}  # everything else (command posts, anti-tank, engineering, medical, vessels, other) -> "Other"

# WarSpotting model names -> GUR teardown family. Order matters: first match wins.
MATCH = [
    ("T-72", r"^T-72B3"),
    ("Orlan-10", r"Orlan-10\b"),
    ("Zala 421-16E", r"421-16"),  # WarSpotting writes "421-16Е" with a Cyrillic Е
    ("Supercam", r"Supercam"),
    ("Eleron-3", r"Eleron-3"),
    ("Fenix", r"'Feniks' reconnaissance UAV|Fenix UAV"),  # not the KamAZ-53949 'Feniks' armoured truck
    ("Kartograf", r"Kartograf"),
    ("Orion UAV", r"\bOrion\b"),
    ("Granat-4", r"Granat-4"),
    ("Forpost-R", r"Forpost"),
    ("Ka-52", r"Ka-52"),
    ("Tor-M2", r"Tor-M2"),
    ("R-330 jammers", r"R-330BMV"),
    ("KamAZ Typhoon-K", r"Typhoon-K"),
]
LOOKALIKE = re.compile(r"T-72|Orlan|ZALA|Supercam|Eleron|Fenix|Kartograf|Orion|Granat|Forpost|Ka-52|Tor-M|R-330|Typhoon", re.I)


def read(name):
    with open(os.path.join(RAW, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SNAP, sorted(os.listdir(SNAP))[-1])
    end = max(r["month"] for r in read("launches.csv"))
    with gzip.open(path, "rt", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["status"] in COUNTED]

    monthly = collections.Counter()
    for r in rows:
        monthly[(r["date"][:7], CATEGORY.get(r["type"], "Other"))] += 1
    with open(os.path.join(RAW, "losses_monthly.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["month", "category", "losses"])
        for (m, c), n in sorted(monthly.items()):
            if m <= end:
                w.writerow([m, c, n])

    pats = [(fam, re.compile(p, re.I)) for fam, p in MATCH]
    by_year = collections.defaultdict(collections.Counter)
    unmatched = collections.Counter()
    for r in rows:
        if r["date"][:7] > end:
            continue
        fam = next((fam for fam, p in pats if p.search(r["model"])), None)
        if fam:
            by_year[fam][r["date"][:4]] += 1
        elif LOOKALIKE.search(r["model"]):
            unmatched[r["model"]] += 1

    old = {r["family"]: r for r in read("matched_losses.csv")}
    out = []
    for fam, _ in MATCH:
        r = dict(old[fam])
        for y in ("2022", "2023", "2024", "2025", "2026"):
            r["l" + y] = by_year[fam][y]
        r["losses"] = sum(by_year[fam].values())
        out.append(r)
    with open(os.path.join(RAW, "matched_losses.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(old[next(iter(old))].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out)

    print(f"{len(rows):,} losses in {os.path.basename(path)}, counted to the end of {end}")
    for r in out:
        print(f"  {r['family']:<16} {r['losses']:>5}  (2025: {r['l2025']}, 2026: {r['l2026']})")
    if unmatched:
        print("Models that look like a matched platform but are not matched (review):")
        for m, n in unmatched.most_common():
            print(f"  {n:>4}  {m}")


if __name__ == "__main__":
    main()
