# Panda Shocks

**The Soft-Power Shock (SPS) series from giant panda births abroad, 24 host jurisdictions, 2004–2025.**

*(DOI placeholder: replace after the first Zenodo release.)*

Zong-Wei Yeh, Department of Finance, National Chung Cheng University (zweyeh@ccu.edu.tw)

## What it is

When a giant panda is born in a foreign zoo, the zoo announces it, the host country's media cover it,
and the host public's interest in China's best-known symbol jumps. The month of a birth is set by
biology, through delayed implantation and frequent pseudo-pregnancies, and no government decides
anything on that date. *Panda Shocks* releases the soft-power shock (SPS): an exogenous rise in a foreign public's exposure to a country's
soft-power asset that carries no change in policy, identified from the births of giant pandas at
foreign zoos and measured as the dose of attention each birth draws.
It measures each birth by the jump in the host's Google search
attention to the giant panda in the three days after the announcement relative to the week before.
The doses are in units of the host's own standard deviation and are summed to a host × month
SPS series. The release contains the SPS series, the 491-event database behind it with sources, hard
political events as a benchmark, breeding attempts, placebo animal events, travel and trade policy
regimes, and every daily Google window used to compute a dose.

Website: `index.html` at the repository root (served by GitHub Pages from `/`). The home page draws
an interactive chart of the SPS by host from `series/sps_series.js`, which `scripts/build_series_js.py`
generates from `data/panda_shocks_monthly.csv`.

## Files

| file | rows | content |
|---|---|---|
| `data/panda_shocks_monthly.csv` | 6,336 | host × month SPS series and variants, monthly Google indices |
| `data/events.csv` | 491 | panda event database (births, deaths, loans, …) with doses, flags, sources |
| `data/hard_events.csv` | 98 | hard political events (conflicts −1, summits/deals +1) |
| `data/attempts.csv` | 144 | announced breeding attempts and their outcomes |
| `data/placebo_animals.csv` | 17 | non-China animal events (Knut, Harambe, Moo Deng, …) |
| `data/policy_regimes.csv` | 139 | tour bans, visa waivers, flight suspensions, FTAs |
| `data/attention_daily_windows.csv` | 244,712 | daily Google windows, rel_day −60…+120 |
| `data/attention_spillover_windows.csv` | 119,641 | daily windows for 14 China-related and placebo topics |
| `documentation/CONSTRUCTION.md` | | definitions, equations, exclusion rules, known issues |
| `documentation/CODEBOOK.md` | | every column of every file |
| `examples/lp_example.py`, `.do` | | panel local projection on the SPS (Python, Stata) |
| `scripts/download_outcomes.md` | | where to get trade, tourism and co-authorship outcomes |

Outcome data such as trade, tourism and co-authorship are **not** included because they fall under
third-party licences. See `scripts/download_outcomes.md`.

## Quick start

```python
import pandas as pd
z = pd.read_csv("data/panda_shocks_monthly.csv")          # host, month (YYYY-MM), z_birth_nat, ...
y = pd.read_csv("my_outcome.csv")                         # host, month, y
df = z.merge(y, on=["host", "month"])
```

```bash
python examples/lp_example.py --synthetic                 # test run on a simulated outcome
python examples/lp_example.py --outcome my_outcome.csv --var y
```

The headline series is `z_birth_nat`, the SPS (national dose), and the paper's sample starts in 2011-01. Over 2011–2025 it
has 33 nonzero host-months in 14 hosts, with a median dose of 3.08 host standard deviations.

## Citation

Please cite the paper and the dataset:

> Yeh, Zong-Wei (2026). "Soft Power Shocks: Does Attention to a Symbol Translate into Bilateral
> Exchange?" Working Paper, Department of Finance, National Chung Cheng University.


BibTeX is in `CITATION.bib`; machine-readable metadata are in `CITATION.cff` and `.zenodo.json`.

## Licence

Data and documentation: CC BY 4.0. Code: MIT. See `LICENSE`. The attention series are derived from
Google Trends.

## Versions

See `CHANGELOG.md`. v1.0 (2026-11) is the first release.
