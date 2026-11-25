# Monthly update

How to add a month to the Burn Rate Index. About an hour, most of it waiting for WarSpotting. Do it once ISIS has published the month, usually around the 10th of the following month.

## 1. Launches and strike share (ISIS)

Source: Institute for Science and International Security, "Monthly Analysis of Russian Shahed 136 Deployment Against Ukraine – Updated", https://isis-online.org/isis-reports/monthly-analysis-of-russian-shahed-136-deployment-against-ukraine-updated (the page is replaced each month; previous months are linked from it).

From the newest report, take for the new month:

- **Launches**: the "reporting baseline" total of Shahed-type UAVs including decoys (Table 1a, "Launches Total UAVs"). Not the General Staff's count of genuine Shaheds, and not ISIS's "working estimate" range.
- **Strike share**: the "% of total" in the Shahed/Geran column of the same table, to two decimals (82.47% → 0.82).

Edit two files:

```
data/raw/launches.csv       add:  YYYY-MM,<launches>,reporting baseline (ISIS report of <date>)
data/raw/strike_share.csv   add:  YYYY-MM,<share>,ISIS monthly (report of <date>; retrieved <date>)
```

If ISIS has not published a strike share for the month, repeat the last ISIS monthly share and write `carried forward from YYYY-MM` in `basis`. Replace it when ISIS publishes.

**Check earlier months too.** ISIS sometimes revises recent months. Compare its table with the last three rows of both files and correct any that changed, noting the revision in `note` or `basis`.

## 2. Losses (WarSpotting)

```
python scripts/fetch_warspotting.py
python scripts/aggregate_losses.py
```

The first command downloads every Russian loss record into `data/raw/warspotting/russia_<today>.csv.gz` (30–40 minutes at one request a second). The second rebuilds `losses_monthly.csv` and `matched_losses.csv` from the newest snapshot, counting losses up to the end of the latest month in `launches.csv`, and prints any new WarSpotting model names that might belong to a matched platform. If it lists any, decide whether they match a GUR teardown and add them to `MATCH` in `scripts/aggregate_losses.py`.

Delete older snapshots in `data/raw/warspotting/` before committing, keeping the newest only (each is about 1 MB).

## 3. Rebuild

```
python scripts/build.py
```

This rewrites `data/derived/` and the headline block in README.md.

## 4. Checks before pushing

1. **The headline makes sense.** `build.py` prints `headline.json`. The latest month and its label are right; the change on the previous month is plausible (launches and the index move together; a large jump should come from launches or the strike share, never from nowhere).
2. **Nothing old moved by accident.** `git diff data/derived/burn_rate_monthly.csv`: only the new month is added, unless you corrected a revision in step 1.
3. **Losses look right.** `git diff --stat data/raw/losses_monthly.csv`. Recent months always grow a little (footage surfaces late). Months more than a year old should barely change.
4. **The dashboard renders.** Run `python -m http.server`, open http://localhost:8000, and check: the hero label shows the new month; the launches chart has a new bar; the window labels say "Jan 2025 to <new month>"; there are no errors in the browser console.
5. **Update the text.** Add a line to the change log in METHODOLOGY.md with the month's index and change. If the strike-share basis changed (for example a month carried forward), update the strike-share table in METHODOLOGY.md.

## 5. Commit and push

```
git add data/ README.md METHODOLOGY.md
git commit -m "Add <Month YYYY>"
git push
```

GitHub Pages republishes the dashboard within a few minutes.
