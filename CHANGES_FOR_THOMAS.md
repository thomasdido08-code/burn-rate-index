# Changes for Thomas: Burn Rate Index

What changed on branch `iaw-prep-2026-12` (25 November 2026), why, and how to defend it.

## Headline numbers, before and after

| Figure | Before (live site) | After strike shares | After October | After loss refresh (final) |
|---|---|---|---|---|
| Latest month | Sep 2026: 738,096 | Sep 2026: 865,331 | **Oct 2026: 813,503** | Oct 2026: 813,503 |
| Change on previous month | +30% | +37% | −6% | −6% |
| EU-owned, latest month | 92,094 | 104,211 | 97,384 | 97,384 |
| Window | Jan 2025–Sep 2026 | same | Jan 2025–Oct 2026 | same |
| Records fired in window | 11.50M | 11.73M | 12.55M | 12.55M |
| Range | 3.1M–16.7M | 3.1M–16.7M | 3.3M–17.7M | 3.3M–17.7M |
| EU-owned in window | 1.44M | 1.47M | 1.56M | 1.56M |
| Records in matched lost platforms | 14,511 | 14,511 | 14,511 | **14,352** |
| Drones vs matched losses | 792× | 809× | 865× | **874×** |
| Documented losses in window | 4,599 | 4,599 | 4,678 | **4,706** |

## 1. ISIS's published strike shares replace the 64% placeholder (Jul–Sep 2026)

**What.** The live site carried ISIS's January–June average (64%) forward for July–September, marked as our assumption. ISIS's report of 10 November 2026 publishes those months: 71%, 74%, 79%, and 82% for October. The method says to use ISIS's monthly share when it exists, so I did.

- *Sceptic: "Your September number jumped 17% overnight."* → Because ISIS published the real share; we had been using a placeholder that we labelled as an assumption. The method didn't change; the data arrived.

**Watch this one: jet drones.** The rising share is mostly jet-powered Geran-3s. The index gives every strike drone the Shahed-136's 155 foreign records, but GUR's Geran-3 teardown has 44. For October alone, ISIS counts at least 2,412 jets; giving those the Geran-3 profile would cut October from 813,503 to 545,771 (−33%). This is now stated as a limit in README and METHODOLOGY, with that sensitivity figure.

- *Sceptic: "Your recent months are inflated by jets."* → Partly, yes, and we say so with a number: up to a third for October. ISIS doesn't publish a full monthly jet split yet. When it does, the index will split them. The direction of the headline doesn't depend on it.

**My recommendation:** split jets out as soon as ISIS's monthly jet counts allow, probably the next methodology change worth making.

## 2. October 2026 added

6,148 launches (ISIS "reporting baseline", the same definition as July–September), 82% strike share. The General Staff separately reported 6,473 genuine Shahed/Geran launches for October (decoys excluded); ISIS says the two are different populations, so the index keeps ISIS's series. October index: **813,503, −6% on September**.

- *Sceptic: "Launches were down 9% in October; did Russia fire less?"* → Not necessarily. ISIS says daytime coverage was incomplete and the baseline is partial. That's why recent months are labelled as possibly revised.

## 3. Losses: a fresh, scripted WarSpotting download

**What.** `scripts/fetch_warspotting.py` downloads every loss record (23,941, retrieved 25 Nov); `scripts/aggregate_losses.py` rebuilds both loss files. They reproduce the 1 November category totals for 2022–2024 to within 4 losses, so the categories are the same as before.

**Two fixes:**
- **Matched losses now cover exactly the same months as launches** (by loss date, to the end of October), instead of whole calendar years. The "slightly favours losses" caveat is gone.
- **Three KamAZ "Feniks" armoured trucks were counted as Fenix drones** in the first version. Removed.

- *Sceptic: "Your loss numbers changed."* → Recent months always grow as footage surfaces (October 2026: 79 → 97). The fix to the matching is documented in the change log.

## 4. UPDATING.md

Step-by-step monthly procedure: which ISIS figures to take, files to edit, two commands for WarSpotting, `build.py`, and five checks before pushing. Window labels on the dashboard and in the README now follow the latest month automatically, so the update only touches data files.

## 5. Dashboard check

Served locally: the hero shows October 2026 (813.5K, −6%, 97.4K EU-owned); every window label reads "Jan 2025 to Oct 2026"; the launches chart has 22 months of bars; the comparison text shows 874×; no console errors.

## 6. DECISION NEEDED: the "~874×" comparison

I have **not** changed the headline wording. It is the easiest line to attack, for three reasons:

1. **Different kinds of thing.** Drones are consumables built to be used up; tanks and jammers are platforms that last. Comparing one with the other is close to comparing ammunition with rifles.
2. **The denominator is small by construction.** Only 14 platform types have GUR teardowns. They account for **287 of the 4,706 losses** documented in the same months (6%). The more types GUR tears down, the smaller the multiplier gets.
3. **Records are not chips or value.** A record is one entry in GUR's list, with no quantity.

The multiplier is also the number most likely to be quoted without the caveats.

**Option A: keep the multiplier, add a "How to read this comparison" paragraph.**
> **How to read this comparison.** Both sides count GUR component records, not chips or money. The drone side covers every Shahed-type drone launched; the loss side covers only the 14 platform types GUR has taken apart, 6% of the losses WarSpotting documented in the same months, and counts each as if rebuilt new, although most lost armour is replaced from storage. The comparison shows where Russia's recurring demand for foreign parts comes from: weapons it fires and must rebuild every time, rather than equipment it loses.

**Option B (recommended): drop the multiplier, show both numbers, add the paragraph above.**
> From January 2025 to October 2026, Shahed-type launches carried an estimated 12.5M foreign component records (range 3.3M to 17.7M), 1.6M from EU-owned firms. The 287 lost platforms that GUR has torn down contained about 14,000, even if each were rebuilt new.

**Option C: a per-month rate.**
> Each month, Russia's Shahed-type launches carry about 570,000 foreign component records: more than were in every matched platform it lost in the whole of 2025 and 2026 combined, forty times over.

C is vivid but stacks two comparisons and invites the same critique as the multiplier.

**Why B.** It keeps the striking contrast (millions against thousands) without a number that depends on how many teardowns GUR happens to have published. Both figures are easy to check and the caveat sits right next to them. A reviewer can still compute the ratio, but we're no longer leading with it.

- *Sceptic (on any option): "So losses don't matter?"* → They matter for Russia's armour, which it replaces mostly from storage. They don't drive its demand for *new* foreign components; what it fires does, and that's what the index measures.

Tell me A, B or C (or edit the wording) and I'll apply it to README, the dashboard text, build.py's headline and METHODOLOGY.md together.

## Ready to go public?

The repo is already public with GitHub Pages. This branch is ready to merge once you choose the comparison wording.
