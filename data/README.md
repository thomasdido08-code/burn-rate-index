# Data dictionary

## raw/

| File | One row per | Columns | Source |
|---|---|---|---|
| `launches.csv` | month | `month` (YYYY-MM), `launched` (Shahed-type drones incl. decoys), `note` | ISIS, from Ukrainian Air Force reports |
| `strike_share.csv` | month | `month`, `strike_share` (0–1), `basis` (where the figure comes from) | ISIS; see METHODOLOGY.md for carried-forward months |
| `unit_profiles.csv` | weapon type | `family`, `gur_entry`, `parts` (all records), `high_priority`, `us`, `eu`, `china`, `other`, `russia_belarus`, `unidentified` (records by manufacturer's home) | GUR War & Sanctions, one teardown per type |
| `losses_monthly.csv` | month × category | `month`, `category`, `losses` (destroyed, captured or abandoned) | WarSpotting, retrieved 1 Nov 2026 |
| `matched_losses.csv` | platform type | `family`, `label`, `kind`, `losses` (whole war), `l2022`–`l2026` (by year), records per unit by origin, `gur_entry` | WarSpotting × GUR |
| `tanks.csv` | year | `year`, `warspotting_tanks`, `iiss_tanks_lost`, `iiss_tanks_fielded` | WarSpotting; IISS Military Balance 2025 |
| `storage.csv` | count | `category`, `date`, `prewar`, `remaining`, `restorable`, `estimator`, `url` | Jompy via Euromaidan Press / UkraNews |
| `production.csv` | estimate | `item`, `date`, `per_month`, `estimator`, `scope`, `url` | Ukrainian intelligence via Kyiv Independent / Militarnyi |
| `other_weapons.csv` | weapon type | `weapon`, `kind`, `records_per_unit`, `used_oct2025`, `used_source`, `gur_url` | GUR; CSIS; Ukrainian General Staff via Militarnyi |
| `tank_new.csv` | estimate | `item`, `per_year`, `estimator`, `url` | Frontelligence Insight via Euromaidan Press |

## derived/ (written by `scripts/build.py`)

| File | Contents |
|---|---|
| `burn_rate_monthly.csv` | The index by month: launches, strike share and its basis, estimated strike and other drones, central/low/high foreign records, central/low/high EU-owned records |
| `headline.json` | Latest month's index and change, window totals, documented losses, matched-loss records and the ratio between them |

To add a month: append a row to `launches.csv` and `strike_share.csv`, then run `python scripts/build.py`.
