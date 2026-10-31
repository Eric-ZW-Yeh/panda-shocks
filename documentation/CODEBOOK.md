# Codebook — Panda Shocks v1.0: the Soft-Power Shock (SPS) series

All files are UTF-8 CSV with a header row, comma-separated, `.` as decimal mark. Missing values are
empty cells. Dates are ISO 8601 (`YYYY-MM-DD`), months `YYYY-MM`. Hosts are ISO 3166-1 alpha-2 codes
(HK and MO for Hong Kong and Macau, TW for Taiwan). Definitions and equations: [CONSTRUCTION.md](CONSTRUCTION.md).

"SD units" means standard deviations of the host's own rescaled daily Google series on non-event days
(CONSTRUCTION.md §3).

| file | rows | unit of observation |
|---|---|---|
| `data/panda_shocks_monthly.csv` | 6,336 | host × month, 24 hosts × 264 months (2004-01 … 2025-12) |
| `data/events.csv` | 491 | dated panda event |
| `data/hard_events.csv` | 98 | dated hard political event |
| `data/attempts.csv` | 144 | publicly announced breeding attempt (zoo × season) |
| `data/placebo_animals.csv` | 17 | non-China animal event |
| `data/policy_regimes.csv` | 139 | host × policy regime spell |
| `data/attention_daily_windows.csv` | 244,712 | event × topic × day (rel_day −60 … +120) |
| `data/attention_spillover_windows.csv` | 119,641 | birth/death × topic × day (rel_day −60 … +120) |

---

## 1. `panda_shocks_monthly.csv`

| column | type | description |
|---|---|---|
| `host` | str | ISO2 host code (24 hosts) |
| `month` | YYYY-MM | calendar month; events are assigned by `date_announce` |
| `z_birth_nat` | float, SD units | **The SPS (national dose); headline series.** Sum of `dose_national` over births with `in_z_birth_nat = 1` announced in the month; 0 in months without such a birth. Source column: `shock_monthly.csv:z_birth_nat`. |
| `z_birth_reg` | float, SD units | **The SPS (regional dose).** Same births, best-of dose (regional window of the zoo where usable, else national; `events.csv:dose_best`). Source column: `shock_monthly.csv:z_birth` (renamed). |
| `z_birth_count` | int | **The SPS (count).** Number of births entering `z_birth_nat` in the month (0/1 in v1.0). Source: `shock_monthly.csv:n_birth`. |
| `z_birth_cap90` | float, SD units | **The SPS (capped dose).** `z_birth_nat` capped from above at 15.7033, the 90th percentile of its nonzero values in 2011-01…2025-12 (computed in the release script). |
| `z_death` | float, SD units (≤ 0) | Minus the sum of best-of doses of deaths with `in_z_death = 1` announced in the month. Source: `shock_monthly.csv:z_death`. |
| `z_hard` | float, China-topic SD units | Sum over in-panel hard events with a measurable intensity of `direction × intensity_china` (see `hard_events.csv`). |
| `n_conflict` | int | Number of in-panel hard events with `direction = −1` announced in the month (all, with or without intensity). |
| `n_summit` | int | Number with `direction = +1`. |
| `A_panda` | float, 0–100 | **Attention to the panda (monthly Google index).** Google Trends monthly index, topic Giant panda (`/m/03bj1`), host geo, 2004-01…2025-12, single pull. |
| `A_china` | float, 0–100 | Same for topic China (`/m/0d05w3`). |

Missing values: every `z_*` and `n_*` is missing in 2004-01 (24 rows; no complete pre-window exists);
zero otherwise in months without an event. `A_*` have no missing values in v1.0 (Google reports 0 for
months with too little volume; QA, MO and KR have many such zeros before 2011).

Nonzero counts: `z_birth_nat` 42 host-months (33 in 2011–2025, in 14 hosts; median nonzero 3.08, max
37.9 = BE 2016-06); `z_death` 11 (10 in 2011+); `z_hard` 88; `n_conflict` 44; `n_summit` 44.

**Not included.** A naming / cub-debut series (`z_naming`) does not exist as a column of the source panel
and is not released; naming and cub-debut doses are available per event in `events.csv`
(`event_type ∈ {naming, cub_debut}`, flag `in_z_bio`), and users can sum them. The paper's broader
biological series `z_bio` (births + namings + cub debuts) can be rebuilt the same way.

## 2. `events.csv`

| column | type | description |
|---|---|---|
| `event_id` | str | `{host}_{YYYYMMDD of date_event}_{event_type}_{k}` |
| `host` | str | ISO2 |
| `zoo` | str | institution |
| `event_type` | str | announce, agreement, arrival, debut, pregnancy, birth, birth_failed, naming, cub_debut, cub_departure, death, return, recall, extension |
| `date_event` | date | physical date (birth, arrival, death, signing …); may be month/year precision |
| `date_announce` | date | first public announcement = day 0 for attention |
| `announce_precision` | str | day / month / year |
| `announce_confidence` | str | `low` for JP and MX announcements before 2011 (often copies of the birth date), else `normal` |
| `panda_names` | str | names, semicolon-separated |
| `n_cubs` | int | births and failed pregnancies (twins = 2) |
| `cub_survived_30d` | 0/1 | births |
| `bundled` | −1/0/+1 | hard-political bundling within ±7 days of `date_announce`: +1 state visit/summit/major agreement, −1 diplomatic conflict/sanction/punitive recall |
| `bundle_note` | str | the bundled event and its date |
| `official_present` | 0/1 | Chinese ambassador or higher attended (naming, debuts, arrival) |
| `trade_delegation` | 0/1 | Chinese trade/business delegation reported in the same week |
| `politically_framed` | 0/1 | death/return/recall covered as a political signal |
| `first_media` | 0/1 | later media day of an already announced cub (excluded from the SPS) |
| `measurement_zero` | 0/1 | Wakayama/Kobe biological event before 2017 (dose treated as missing) |
| `gt_region` | str | Google regional code used for the regional window (empty if none) |
| `usable_nat`, `usable_reg`, `usable_china` | 0/1 | window usable: share of zero days < 0.5 and scale check passed |
| `zero_share_nat`, `zero_share_reg` | float | share of zero days in the window |
| `dose_national` | float, SD units | $n_e$ on the national panda topic (computed whenever a window exists, usable or not) |
| `dose_regional` | float, SD units | $n_e$ on the regional panda topic |
| `dose_best` | float, SD units | regional if usable, else national if usable, else missing |
| `dose_source` | str | region / national / none |
| `dose_china` | float, SD units | $n_e$ on the national China topic |
| `coverage_reason` | str | usable, precision, pre2004, zero_share, scale_or_sd, measurement_zero |
| `in_z_birth_nat` | 0/1 | enters `z_birth_nat` (42 rows; 33 in 2011+) |
| `in_z_birth` | 0/1 | enters `z_birth_reg` (42) |
| `in_z_bio` | 0/1 | clean, measurable birth/naming/cub_debut (105) |
| `in_z_death` | 0/1 | enters `z_death` (11) |
| `in_z_all` | 0/1 | measurable dose, any type (351) |
| `source_1`, `source_2` | url | primary sources (every row has `source_1`; 346 have `source_2`) |
| `notes` | str | sourcing decisions; `first_media …`, "announce assumed same day", Wikipedia-only rows |

Event counts by type: pregnancy 75, birth 67, cub_debut 54, naming 46, arrival 45, cub_departure 33,
debut 30, extension 28, announce 25, death 24, birth_failed 24, return 21, agreement 17, recall 2.
Bundling: 446 rows 0, 40 rows +1, 5 rows −1.

## 3. `hard_events.csv`

| column | type | description |
|---|---|---|
| `hard_event_id` | str | `H_{host}_{YYYYMMDD}_{category}_{k}` |
| `host` | str | ISO2 (includes a few non-panel countries) |
| `date_announce` | date | date of the event / first report |
| `announce_precision` | str | day / month |
| `direction` | −1/+1 | −1 conflict, +1 rapprochement |
| `category` | str | dalai_lama (20), sanction_or_boycott (11), taiwan_related (8), territorial (7), human_rights (5), arrest_or_detention (3), summit_deal (44) |
| `event` | str | description |
| `in_panel` | 0/1 | host is one of the 24 panel hosts (88 rows) |
| `intensity_china` | float, China-topic SD units | $n_k$ on the China topic; missing if ≥ 50% zero days (88 non-missing) |
| `zero_share_china` | float | share of zero days in the China window |
| `intensity_hint` | str | qualitative note on salience |
| `source_1`, `source_2` | url | sources |
| `notes` | str | |

## 4. `attempts.csv`

| column | type | description |
|---|---|---|
| `attempt_id` | str | `{host}_{year}_{row}` (assigned in the release) |
| `host`, `zoo`, `year` | | breeding season |
| `date_attempt_announce` | date | first announcement of mating / artificial insemination |
| `date_pregnancy_announce` | date | announcement of suspected pregnancy, if any |
| `outcome` | str | live_birth (53), pseudo_pregnancy (40), no_pregnancy (27), stillbirth_or_resorption (10), neonatal_death (3), unknown (11) |
| `linked_event_id` | str | the birth row in `events.csv` for live births |
| `date_outcome_announce`, `outcome_source`, `outcome_detail` | | first public statement of the outcome; `outcome_detail` marks contemporaneous / retrospective / undated |
| `source_1`, `source_2`, `notes` | | |
| `control_group` | str | success (53) / fail (64) / drop (27): the paper's rule — fail = pseudo-pregnancy, stillbirth/resorption, neonatal death, and no-pregnancy rows with a contemporaneous, dated attempt announcement |

## 5. `placebo_animals.csv`

| column | description |
|---|---|
| `placebo_id` | `P_{host}_{YYYYMMDD}_{event_type}` |
| `host`, `date_announce`, `announce_precision`, `animal`, `zoo`, `event_type` | event (birth, debut, death, viral) |
| `gt_query`, `gt_topic_title` | Google topic id (or keyword) and title used for the own-topic window |
| `intensity_own_topic` | $n_e$ on the animal's own topic, in host panda-topic SD units (13 non-missing) |
| `intensity_panda_topic` | $n_e$ on the panda topic in the same window |
| `zero_share_own_topic` | share of zero days in the own-topic window |
| `source_url`, `notes` | |

## 6. `policy_regimes.csv`

| column | description |
|---|---|
| `host` | ISO2 |
| `start_month`, `end_month` | YYYY-MM; empty end = still in force at end-2025 |
| `type` | host_visa (39), cn_tourban (28), fta (27), flights_suspend (22), cn_visafree (20), fta_suspend (2), flights_resume (1) |
| `direction` | +1 eases travel/trade with China, −1 restricts |
| `source_url` | primary source |
| `note` | dates, announcements, cross-checks |

## 7. `attention_daily_windows.csv`

One row per event × topic × day. 212,856 rows for panda events (413 events) and 31,856 rows for hard
events (88 events).

| column | description |
|---|---|
| `event_set` | `panda_event` (id in `events.csv`) or `hard_event` (id in `hard_events.csv`) |
| `event_id` | event id |
| `host` | ISO2 |
| `topic` | `panda` (national), `china` (national), `panda_region` (zoo region) |
| `region` | Google regional code for `panda_region` rows |
| `date`, `rel_day` | calendar day and day relative to `date_announce` (−60 … +120) |
| `value_raw` | Google Trends daily value as returned (0–100 within the request) |
| `value_rescaled` | `value_raw × s_w`, on the scale of the monthly index (CONSTRUCTION.md §3) |
| `value_std` | `value_rescaled / σ_host,topic` (SD units); missing where σ is undefined (sparse hosts/regions, TW-TPE) — 17,195 rows |
| `window_usable` | 1 if the window has < 50% zero days and passed the scale check (hard events: zero-share rule only) |

## 8. `attention_spillover_windows.csv`

Daily windows for 48 events, announced 2012-07 onward (33 births and 10 deaths from `events.csv`, 5
placebo-animal events from `placebo_animals.csv`), on 14 topics, used for the paper's spillover tests:
`panda`, `china`; brands `huawei`, `xiaomi`, `tiktok`, `shein`; travel `chengdu`, `greatwall`; language
`mandarin`; culture `cny` (Chinese New Year), `cuisine`; placebo countries `japan`, `skorea`,
`thailand`. Columns as in §7 plus `topic_group` (brands, travel, language, culture, china, panda,
placebo_countries). `value_std` = `value_rescaled` divided by the host SD of that topic, missing when
the window is unusable. For births and deaths the `panda` and `china` rows are the §7 windows (same SD);
for the placebo events the `panda` rows hold the animal's **own** topic, in host panda-topic SD units.
Topic ids: Huawei `/m/01qkl1`, Xiaomi `/m/0h6955b`, TikTok `/g/11f555cn8l`, SHEIN `/g/11g21kpwrc`,
Chengdu `/m/016v46`, Great Wall `/m/0d2dq0`, Mandarin `/m/03115z`, Chinese New Year `/m/012m47`,
Chinese cuisine `/m/01xw9`, Japan `/m/03_3d`, South Korea `/m/06qd3`, Thailand `/m/07f1x`.

## 9. What is not in the release

No outcome data (trade, tourism, co-authorship, flights, FDI) are distributed, because they are covered by
third-party licences. `scripts/download_outcomes.md` lists the sources and what to download.
