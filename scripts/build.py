#!/usr/bin/env python3
"""Rebuild the Burn Rate Index from the raw data files.

Reads data/raw/*.csv, writes:
  data/derived/burn_rate_monthly.csv  the index, month by month
  data/derived/headline.json          the headline figures
and refreshes the headline block in README.md.

Standard library only. Run from the repository root:  python scripts/build.py
The same arithmetic runs in the browser in index.html; this script is the
reference and the place to check it.
"""
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data", "derived")

SHAHED = "Shahed-136 / Geran-2"
GERBERA = "Gerbera (decoy)"
WINDOW_START = "2025-01"  # window runs from here to the latest month in launches.csv
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def read(name):
    with open(os.path.join(RAW, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(x):
    return float(x) if x not in ("", None) else 0.0


def foreign(row):
    """Records attributed to US, EU, Chinese or other foreign parent groups.
    Excludes Russia/Belarus and unidentified records."""
    return num(row["us"]) + num(row["eu"]) + num(row["china"]) + num(row["other"])


def label(month):
    return f"{MONTHS[int(month[5:7]) - 1]} {month[:4]}"


def main():
    launches = read("launches.csv")
    share = {r["month"]: num(r["strike_share"]) for r in read("strike_share.csv")}
    basis = {r["month"]: r["basis"] for r in read("strike_share.csv")}
    profiles = {r["family"]: r for r in read("unit_profiles.csv")}
    matched = read("matched_losses.csv")
    losses = read("losses_monthly.csv")

    sh, ge = profiles[SHAHED], profiles[GERBERA]
    sh_f, ge_f = foreign(sh), foreign(ge)
    sh_eu, ge_eu = num(sh["eu"]), num(ge["eu"])

    monthly = []
    for r in sorted(launches, key=lambda r: r["month"]):
        m = r["month"]
        if m not in share:
            raise SystemExit(f"No strike share for {m}: add a row to data/raw/strike_share.csv")
        n, s = num(r["launched"]), share[m]
        strike = round(n * s)
        monthly.append({
            "month": m,
            "launched": int(n),
            "strike_share": s,
            "strike_share_basis": basis[m],
            "strike_est": strike,
            "other_est": int(n) - strike,
            "index_central": round(n * (s * sh_f + (1 - s) * ge_f)),
            "index_low": round(n * ge_f),
            "index_high": round(n * sh_f),
            "eu_central": round(n * (s * sh_eu + (1 - s) * ge_eu)),
            "eu_low": round(n * ge_eu),
            "eu_high": round(n * sh_eu),
            "launch_note": r.get("note", ""),
        })

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "burn_rate_monthly.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(monthly[0].keys()))
        w.writeheader()
        w.writerows(monthly)

    window = (WINDOW_START, monthly[-1]["month"])
    win = [r for r in monthly if window[0] <= r["month"] <= window[1]]
    tot = lambda k: sum(r[k] for r in win)
    # matched_losses.csv is counted up to the end of the latest month (scripts/aggregate_losses.py),
    # so summing the window's calendar years covers exactly the window.
    years = [f"l{y}" for y in range(int(window[0][:4]), int(window[1][:4]) + 1)]
    lost_units = {r["family"]: sum(num(r.get(y)) for y in years) for r in matched}
    lost_records = sum(n * foreign(profiles[f]) for f, n in lost_units.items())
    lost_eu = sum(n * num(profiles[f]["eu"]) for f, n in lost_units.items())
    latest, previous = monthly[-1], monthly[-2]

    headline = {
        "latest_month": latest["month"],
        "latest_label": label(latest["month"]),
        "index_latest": latest["index_central"],
        "index_previous": previous["index_central"],
        "previous_label": label(previous["month"]),
        "change_vs_previous": round((latest["index_central"] - previous["index_central"]) / previous["index_central"], 4),
        "eu_latest": latest["eu_central"],
        "window": f"{window[0]} to {window[1]}",
        "window_label": f"{label(window[0])} to {label(window[1])}",
        "launches_window": tot("launched"),
        "strike_window": tot("strike_est"),
        "index_window_central": tot("index_central"),
        "index_window_low": tot("index_low"),
        "index_window_high": tot("index_high"),
        "eu_window_central": tot("eu_central"),
        "documented_losses_window": int(sum(num(r["losses"]) for r in losses if window[0] <= r["month"] <= window[1])),
        "matched_platforms_lost_window": int(sum(lost_units.values())),
        "matched_lost_records": int(lost_records),
        "matched_lost_eu": int(lost_eu),
        "drones_vs_matched_losses": round(tot("index_central") / lost_records),
    }
    with open(os.path.join(OUT, "headline.json"), "w", encoding="utf-8") as f:
        json.dump(headline, f, indent=2)

    update_readme(headline)
    print(json.dumps(headline, indent=2))


def compact(n):
    for size, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= size:
            return f"{n / size:.1f}".rstrip("0").rstrip(".") + suffix
    return f"{n:,.0f}"


def update_readme(h):
    path = os.path.join(ROOT, "README.md")
    if not os.path.exists(path):
        return
    sign = "+" if h["change_vs_previous"] >= 0 else "−"
    block = (
        "<!-- HEADLINE:START (generated by scripts/build.py, do not edit by hand) -->\n"
        f"**{h['latest_label']}: {h['index_latest']:,} foreign component records fired** "
        f"({sign}{abs(h['change_vs_previous']):.0%} on {h['previous_label']}), "
        f"{h['eu_latest']:,} of them from EU-owned firms.\n\n"
        f"From {h['window_label']}, Shahed-type launches carried an estimated "
        f"{compact(h['index_window_central'])} foreign component records "
        f"(range {compact(h['index_window_low'])} to {compact(h['index_window_high'])}), "
        f"{compact(h['eu_window_central'])} from EU-owned firms. "
        f"The {h['matched_platforms_lost_window']:,} lost platforms that GUR has torn down contained about "
        f"{round(h['matched_lost_records'], -3):,}, even if each were rebuilt new.\n\n"
        f"*How to read this comparison.* Both sides count GUR component records, not chips or money. "
        f"The drone side covers every Shahed-type drone launched; the loss side covers only the 14 platform "
        f"types GUR has taken apart, {h['matched_platforms_lost_window'] / h['documented_losses_window']:.0%} "
        f"of the {h['documented_losses_window']:,} losses WarSpotting documented in the same months, and counts "
        f"each as if rebuilt new, although most lost armour is replaced from storage. The comparison shows where "
        f"Russia's recurring demand for foreign parts comes from: weapons it fires and must rebuild every time, "
        f"rather than equipment it loses.\n"
        "<!-- HEADLINE:END -->"
    )
    text = open(path, encoding="utf-8").read()
    new = re.sub(r"<!-- HEADLINE:START.*?<!-- HEADLINE:END -->", block, text, flags=re.S)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)


if __name__ == "__main__":
    main()
