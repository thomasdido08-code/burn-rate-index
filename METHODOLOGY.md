# Methodology

This page sets out how every figure in the Burn Rate Index is produced, what it assumes, and where it is weakest. All arithmetic is in [`scripts/build.py`](scripts/build.py) and runs again in the browser in [`index.html`](index.html); the two give the same results.

## 1. The index

For each month *m*:

```
index(m)   = L(m) × [ s(m) × F_shahed + (1 − s(m)) × F_gerbera ]
low(m)     = L(m) × F_gerbera          (every launch a decoy)
high(m)    = L(m) × F_shahed           (every launch a Shahed-136)
EU index   = same formula with EU-owned records E_shahed, E_gerbera
```

| Symbol | Meaning | Value | Source |
|---|---|---|---|
| L(m) | Shahed-type drones launched in month *m*, decoys included | `data/raw/launches.csv` | ISIS, from Ukrainian Air Force reports |
| s(m) | Share of launches that were strike drones | `data/raw/strike_share.csv` | ISIS |
| F_shahed | Foreign component records in one Shahed-136 / Geran-2 | 155 | GUR War & Sanctions |
| F_gerbera | Foreign component records in one Gerbera decoy | 29 | GUR War & Sanctions |
| E_shahed, E_gerbera | Of which from EU-owned manufacturers | 18, 6 | GUR War & Sanctions |

### What a "component record" is

GUR's War & Sanctions database lists each component found in a teardown as one record: name and marking, manufacturer, and the country where the manufacturer is headquartered. There is no quantity field, and the same part type can appear several times. A record count is therefore a measure of how far a weapon depends on foreign components, not a count of chips.

"Foreign" means records attributed to the United States, EU countries, China and other countries. Records attributed to Russia or Belarus, and records GUR could not attribute, are excluded (`unit_profiles.csv`, columns `russia_belarus` and `unidentified`).

"EU-owned" means the manufacturer's parent group is headquartered in an EU member state. It does not mean the part was made in the EU, sold by an EU firm or exported from the EU. Such parts typically reach Russia through distributors in third countries.

### Strike share

| Months | Value used | Basis |
|---|---|---|
| Jan–Aug 2025 | 59% | ISIS 2025 full-year share, from official data (32,200 strike drones of 54,538 launches) |
| Sep 2025 – May 2026 | 58–66%, month by month | ISIS monthly figures |
| Jun 2026 | 64% | ISIS estimate |
| Jul–Oct 2026 | 71%, 74%, 79%, 82% | ISIS monthly, from its report of 10 November 2026 ([link](https://isis-online.org/isis-reports/monthly-analysis-of-russian-shahed-136-deployment-against-ukraine-updated), retrieved 25 November 2026). July–September replace the 64% carried forward in the first version. |

If ISIS has not yet published a share for the latest month, the last published ISIS monthly share is carried forward and marked in `strike_share.csv`. That is this project's assumption, not ISIS's.

**Jet-powered drones.** Since mid-2026 a growing part of the strike share is jet-powered Geran-3s. ISIS counts them as strike drones, and the index applies the Shahed-136's 155 foreign records to every strike drone. GUR's Geran-3 teardown shows 44. So the rise in the strike share pushes recent months up more than the parts inside the jets justify. ISIS does not publish a full monthly split of jets from piston Shaheds, so the index does not split them yet; see section 6. For October 2026 alone, ISIS directly identifies at least 2,412 jets in the daily reports. Counting those 2,412 with the Geran-3 profile instead would lower October from 813,503 to 545,771 foreign records (−33%). That is a sensitivity figure, not the index.

### Launches in recent months

From July 2026, ISIS calls its monthly total a "reporting baseline": the sum of the Air Force's morning reports and the separately published daytime reports, which do not cover every day. For October 2026 the baseline is 6,148. The General Staff separately reported 6,473 genuine Shahed/Geran launches for October (decoys excluded), and ISIS warns that the two counts are different populations and must not be mixed. The index keeps the ISIS baseline for consistency with earlier months, so recent months are, if anything, low.

The non-strike share includes Garpiya-A1 strike drones and Italmas decoys as well as Gerbera decoys, because official reporting does not separate them. Treating all of them as Gerbera undercounts components, so the central estimate is, if anything, low.

Since May 2026, Ukrainian official reports no longer consistently separate strike drones from the total, so future strike shares depend on ISIS's own estimates.

## 2. Losses and the same-window comparison

- **All losses** (`losses_monthly.csv`): every Russian loss in WarSpotting's database, retrieved through its API on 25 November 2026 (`scripts/fetch_warspotting.py`; snapshot in `data/raw/warspotting/`), excluding damaged vehicles, grouped into eight categories by `scripts/aggregate_losses.py` (armoured vehicles: infantry fighting and mobility vehicles; artillery: towed, self-propelled and rocket; air defence: anti-aircraft systems, radars and jammers; aircraft: aeroplanes and helicopters). Each loss is confirmed by a photo or video, so this is a floor. Recent months are undercounted because footage surfaces late.
- **Matched losses** (`matched_losses.csv`): the 14 WarSpotting platform types that GUR has torn down, with losses per year. Models are matched to GUR weapon families by name. "T-72" means T-72B3 variants only; "R-330 jammers" means the R-330BMV; "Fenix" means the Feniks reconnaissance drone only (the first version also counted three KamAZ-53949 "Feniks" armoured trucks by mistake).

The headline comparison covers January 2025 to the latest month on both sides: matched losses are counted by loss date up to the end of that month. The matched platforms are a small part of what Russia loses: 287 of the 4,706 losses documented from January 2025 to October 2026 (6%).

Matched-loss records are calculated as if every lost unit were replaced with a new build. That is an upper bound: most lost armour has been replaced from storage, which reuses most of the vehicle.

## 3. Resupply

- **Storage** (`storage.csv`): satellite counts of Russian storage bases by the OSINT analyst Jompy, reported by Euromaidan Press (tanks: 7,342 pre-war, 2,478 in October 2025, 2,088 in June 2026 of which 851 judged restorable) and UkraNews (IFVs, APCs, artillery in October 2025). Vehicles kept under roofs are not visible.
- **Pulled from storage vs confirmed lost** (February 2022 – October 2025): pre-war stock minus the October 2025 count, against WarSpotting losses over the same period. Storage drawdown is an upper bound on refurbishment, since some vehicles are stripped for parts. Stored artillery includes mortars and anti-aircraft guns, which WarSpotting's artillery category does not, so that pair is the weakest comparison.
- **Tanks per year** (`tanks.csv`): WarSpotting confirmed tank losses by year; IISS estimates for 2024 (about 1,400 lost, more than 1,500 fielded). The IISS figures for 2025 are not publicly available.
- **New-build tanks** (`tank_new.csv`): about 250 T-90M a year, from leaked Uralvagonzavod documents reported by Frontelligence Insight.

## 4. Missiles and glide bombs (not in the index)

Monthly launch counts by missile type are not published for the whole period, so missiles and glide bombs are left out of the index. `other_weapons.csv` gives GUR records per unit (Kh-101: 138; Iskander-M: 177; Kh-59M2: 37; UMPK-PD glide kit: 8) and the numbers used in October 2025 (74 cruise missiles and 148 ballistic missiles per CSIS; 5,328 guided bombs per the Ukrainian General Staff).

For October 2025, Kh-101 stands in for all cruise missiles, Iskander-M for all ballistic missiles and the UMPK-PD kit for all glide bombs. These GUR totals include some Russian-made records, so they are upper bounds. On that basis, missiles and glide bombs would raise October 2025's figure by about 15%.

## 5. Production estimates

Ukrainian intelligence estimates of strike-drone production: about 2,700 Shahed-type a month (September 2025, via Kyiv Independent) and about 2,800 Geran-2 a month (August 2026, via Militarnyi). They are shown as points at the date each was made, not as constant rates.

## 6. What this is not

- **Not a trade measure.** These are components embedded in weapons Russia used or lost, not import volumes.
- **Not a count of chips.** See "What a component record is" above.
- **Not a measure of where parts were made.** Attribution is by the manufacturer's parent group.
- **Not adjusted for jet-powered Geran-3s.** They are counted with the Shahed-136 profile (155 foreign records) although GUR's Geran-3 teardown has 44. This overstates months with many jets.

## Change log

- **November 2026**: first public version.
- **25 November 2026**: July–September 2026 strike shares changed from the carried-forward 64% to ISIS's published monthly figures (71%, 74%, 79%).
- **25 November 2026**: October 2026 added (6,148 launches, 82% strike share, ISIS report of 10 November 2026). October index: 813,503 foreign records, −6% on September.
- **25 November 2026**: WarSpotting losses retrieved again (25 November instead of 1 November), through the new download and aggregation scripts. Matched losses are now counted by loss date up to the end of the latest month, not by calendar year. Feniks armoured trucks removed from the Fenix drone family. Records in matched losses January 2025–October 2026: 14,511 → 14,352; drones-to-matched-losses ratio 865 → 874. Documented losses in the window: 4,678 → 4,706. September 2026 rose from 738,096 to 865,331 foreign records; January 2025–September 2026 from 11.50M to 11.73M; the drones-to-losses ratio from 792 to 809.
