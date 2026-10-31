# Changelog

Release title: *Panda Shocks: the Soft-Power Shock (SPS) series from giant panda births abroad, 2004–2025*.

## v1.0 — 2026-11

First public release, accompanying Yeh (2026), *Soft Power Shocks: Does Attention to a Symbol Translate
into Bilateral Exchange?*

* `panda_shocks_monthly.csv`: 24 hosts × 2004-01…2025-12; the SPS (national dose) `z_birth_nat`
  (33 nonzero host-months in 14 hosts over 2011–2025, median dose 3.08 host SD), variants
  `z_birth_reg` (the SPS, regional dose), `z_birth_count` (the SPS, count), `z_birth_cap90` (the SPS,
  capped dose), `z_death`, `z_hard`, `n_conflict`, `n_summit`,
  monthly Google indices `A_panda` (attention to the panda) and `A_china`.
* `events.csv`: 491 dated panda events (1994–2025) with announcement dates, bundling codes, doses,
  inclusion flags and sources.
* `hard_events.csv` (98), `attempts.csv` (144), `placebo_animals.csv` (17), `policy_regimes.csv` (139).
* `attention_daily_windows.csv`, `attention_spillover_windows.csv`: daily Google windows, rel_day
  −60…+120.
* The SPS series is frozen at the build used in the paper. 17 later additions to the event database
  (14 `birth_failed` and 3 `pregnancy` announcements, found while resolving breeding-attempt outcomes)
  are not part of v1.0; they do not affect any birth-based series and are scheduled for v1.1.

## Planned

* **v1.1 (2027)**: add the 17 pending events; repeat each Google Trends pull three times and average.
* **Annual updates (each first quarter)**: extend the panel by one year (births, deaths, hard events,
  policy regimes), with a new Google pull for the added year.
