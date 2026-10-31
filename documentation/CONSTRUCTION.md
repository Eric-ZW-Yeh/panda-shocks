# Construction of the Soft-Power Shock (SPS) series

Version 1.0 (November 2026). This note defines every series in the release in words and equations.
It follows Sections 2 and 3 of Yeh (2026), *Soft Power Shocks: Does Attention to a Symbol Translate into
Bilateral Exchange?* Column-level detail is in [CODEBOOK.md](CODEBOOK.md).

## 1. What the shock is

A giant-panda birth in a foreign zoo is a dated event whose timing is set by biology. In giant pandas
implantation of the embryo is delayed by a variable amount and pseudo-pregnancies are common, so the
month of a birth is hard to predict, both for the public and often for the keepers. The first
announcement comes from the zoo and no government decides anything on that date. The birth raises the
host public's attention to the panda, the best-known symbol of China. The soft-power shock (SPS) is an
exogenous rise in a foreign public's exposure to a country's soft-power asset that carries no change
in policy. *Panda Shocks* identifies it from the births of giant pandas at foreign zoos and measures it
as the dose of attention each birth draws, event by event, adding the events up to a host × month
SPS series.

The release covers 24 host jurisdictions (AT, AU, BE, CA, DE, DK, ES, FI, FR, GB, HK, ID, JP, KR, MO,
MX, MY, NL, QA, RU, SG, TH, TW, US) from January 2004 to December 2025.

## 2. Event database

`events.csv` records 491 dated events in the lives of the pandas on loan to the 24 hosts, 1994–2025:
loan announcements and agreements, arrivals, debuts, pregnancies, births, failed pregnancies,
namings, cub debuts, cub departures, extensions, returns, recalls and deaths. Each row has

* the physical date of the event (`date_event`) and the date of its **first public announcement**
  (`date_announce`): a zoo release, a ministry statement or the first wire story. The announcement
  date is day 0 for attention. It is taken from dated sources and never from the location of the peak
  in the search data;
* a **bundling** code: $+1$ if a state visit, summit or major trade or investment agreement between
  the host and China took place within ±7 days of the announcement, $-1$ if a diplomatic conflict,
  sanction or punitive recall did, and $0$ otherwise;
* at least one source URL (zoo release, wire service, national broadcaster or, for 55 rows, a
  Wikipedia page only, which the `notes` say).

Bundling is common for government decisions and rare for biology: 18 of the 25 loan announcements are
bundled, against one of the 67 births (the Berlin twins of 2019, four days before Chancellor Merkel's
visit to China).

## 3. Daily attention

**Source.** Google Trends, topic entity *Giant panda* (`/m/03bj1`), which pools searches for the animal
in every language and script. The topic *China* (`/m/0d05w3`) is the comparison series. Topic entities
are used rather than keywords: in South Korea the English keyword "panda" is zero on most days, while
the topic has a value on all but two of 122 days around Fu Bao's birth.

**Monthly index.** For each host and topic, the monthly index $A_{i,t}$ for 2004-01 to 2025-12, as
Google reports it (0–100, maximum 100 within each host).

**Daily windows.** For each event announced on day $d_e \ge$ 2004-02-01 with day precision, a daily
window from $d_e-60$ to $d_e+120$ (181 days, below Google's 269-day limit for daily data), for the
national panda topic, the national China topic and, where Google reports it, the panda topic in the
region of the zoo (ISO 3166-2 code; Google accepts only the legacy codes FR-F for Centre-Val de Loire
and MX-DIF for Mexico City).

**Rescaling.** Google scales each request so that its maximum is 100, so a window is on its own scale.
Let $v_{w,d}$ be the raw value on day $d$ of window $w$ and $\bar v_{w,m}$ its mean over calendar month
$m$ (only months with at least 20 days inside the window, usually five or six). The scale factor is the
slope of a regression through the origin of the host's monthly index on the window's monthly means,

$$
s_w = \frac{\sum_m A_{i,m}\,\bar v_{w,m}}{\sum_m \bar v_{w,m}^2},
\qquad \tilde v_{w,d} = s_w\, v_{w,d},
$$

computed only if at least three months overlap and the window is not all zeros (`scale_ok`). For the
regional topic the monthly index of the region is used; for the China topic, the monthly China index.

**Standardisation.** The host standard deviation $\sigma_i$ is the standard deviation (ddof = 1) of
$\tilde v_{w,d}$ pooled over all *usable* windows of host $i$ and topic, on **non-event days** only:
days outside $[-10, +40]$ of every dated event of that host. A window is usable if fewer than half
of its days are zero and it passed the scale check. The standardised attention is

$$
a_{i,d} = \tilde v_{w,d} / \sigma_i .
$$

One unit of $a_{i,d}$ means the same thing in every host: one standard deviation of that host's
ordinary daily fluctuation in interest in the panda. Regional series get their own regional
$\sigma$. Regional Taipei City windows (TW-TPE) are not used, because Google files almost no data
under that code.

## 4. Event intensity (the dose)

For event $e$ in host $i$ announced on day $d_e$,

$$
n_e = \frac{1}{3}\sum_{d=0}^{2} a_{i,d_e+d} \;-\; \frac{1}{5}\sum_{d=-7}^{-3} a_{i,d_e+d}.
$$

The post window includes the two days after the announcement so that late-evening announcements, which
reach Google's UTC data on the next day, are captured. The pre window ends on day −3 so that leaks and
late announcements do not enter the baseline. Three versions are stored per event:

| version | column in `events.csv` | definition |
|---|---|---|
| national | `dose_national` | $n_e$ on the national panda topic |
| regional / best-of | `dose_best` (`dose_regional`) | $n_e$ on the zoo's regional series if that window is usable, otherwise the national one (`dose_source`) |
| China | `dose_china` | $n_e$ on the national China topic |

## 5. The monthly SPS series

Let $\mathcal B_{i,t}$ be the set of births announced in host $i$ in month $t$ that pass the
inclusion rules below. The headline series, the SPS (national dose), is

$$
z_{i,t} = \sum_{e \in \mathcal B_{i,t}} n_e^{\text{national}},
$$

and $z_{i,t} = 0$ in months without such a birth (`z_birth_nat`). Variants:

* `z_birth_reg`, the SPS (regional dose): the same sum with the best-of (regional where usable) dose;
* `z_birth_count`, the SPS (count): the number of births in $\mathcal B_{i,t}$ (no dose);
* `z_birth_cap90`, the SPS (capped dose): `z_birth_nat` capped at the 90th percentile of its nonzero values over 2011–2025
  (15.70);
* `z_death`: $-\sum n_e$ over deaths announced in the month that pass the same rules (best-of dose,
  negative sign);
* `z_hard`: signed intensity of hard political events (Section 6).

**Inclusion rules.** A birth enters $\mathcal B_{i,t}$ only if all of the following hold:

1. **Not bundled.** Biological events (birth, naming, cub debut, death, failed pregnancy) with a
   bundling code $\neq 0$ are excluded (one birth, three deaths and three namings in the database).
2. **Not a later media day.** Rows recording a later media date of the same cub (first veterinary
   examination, sex reveal, first photograph or video; `first_media = 1`) are excluded.
3. **Measurable dose.** The announcement has day precision and falls on or after 2004-02-01, a daily
   window exists, and the national window is usable (fewer than half of its days zero, scale check
   passed).
4. **Not a measurement zero.** Biological events at Adventure World (Shirahama, Wakayama) and the Kobe
   Oji Zoo announced before 2017-01-01 are treated as missing doses rather than small ones: Google's
   topic entity captured Japanese-script searches poorly before 2017 and these zoos are invisible in
   the national series. Births at Ueno Zoo in Tokyo are visible and stay in.

`events.csv` carries the resulting flags (`in_z_birth_nat`, `in_z_birth`, `in_z_death`, …) and a
`coverage_reason` for every excluded row.

**Sample.** The instrumental-variable sample used in the paper starts in **2011-01**. Before 2011 most
birth windows are too sparse to measure a dose (median post/pre ratio 1.4). The monthly file covers
2004-02 onward so that users can choose; all `z_*` are missing in 2004-01, the month in which no
complete pre-window can exist.

In 2011–2025 the SPS (national dose) has **33 nonzero host-months in 14 hosts**, with a median dose of
**3.08** host standard deviations; the largest are Belgium 2016-06 (37.9) and France 2017-08.

## 6. Hard political events

`hard_events.csv` lists 98 dated hard political events between China and the hosts (and a few other
countries, `in_panel = 0`), coded by **direction**:

* $-1$ **conflict**: official meetings of heads of state or government with the Dalai Lama (20),
  sanctions and boycotts, Taiwan-related disputes, territorial disputes, arrests and detentions,
  human-rights conflicts (54 in total);
* $+1$ **rapprochement**: summits, state visits and major agreements (44).

The intensity of hard event $k$ is measured like that of a birth but on the **China** topic,
$n_k^{\text{China}}$, in host China-topic SD units; it is missing if the window has half or more zero
days. The monthly series are

$$
z^{\text{hard}}_{i,t} = \sum_{k \in \mathcal H_{i,t}} \text{direction}_k \cdot n_k^{\text{China}},
\qquad
n^{\text{conflict}}_{i,t} = \#\{k \in \mathcal H^{\text{all}}_{i,t}: \text{direction}_k = -1\},
$$

and likewise `n_summit` for $+1$. The counts use every in-panel hard event, with or without a
measurable intensity. Hard events are chosen by governments and are **not** exogenous; in the paper they
serve as a positive control.

## 7. Companion files

* `attempts.csv`: 144 publicly announced breeding attempts with their outcome (live birth,
  pseudo-pregnancy, stillbirth or resorption, neonatal death, no pregnancy, unknown) and the
  `control_group` assignment used in the paper (success / fail / drop): failed = pseudo-pregnancy,
  stillbirth or resorption, neonatal death, and no-pregnancy rows whose attempt was announced at the
  time.
* `placebo_animals.csv`: 17 non-China animal events that drew national attention (Knut, Harambe,
  Marius, Moo Deng, …) with the intensity on their own Google topic.
* `policy_regimes.csv`: 139 dated policy regimes affecting travel and trade with China (Chinese
  group-tour bans, visa waivers in both directions, flight suspensions, FTAs), with source URLs.
* `attention_daily_windows.csv` and `attention_spillover_windows.csv`: the daily data behind every
  dose.

## 8. Known measurement issues

* **Japan before 2017.** Japanese attention to the panda (monthly Google index) averages about 6 before 2017 and about 44 after; it
  jumps permanently with the birth of Xiang Xiang at Ueno in June 2017. This reflects the coverage of
  Japanese-script searches by Google's topic entity, not a change in interest. Pre-2012 Japanese daily
  windows have 57–96 percent zero days. Hence rule 4 above. Taiwan (12 → 53) and Macau (series starts
  in 2011) show milder versions.
* **Spain and Mexico, 2004–2006.** The panda topic is very high in 2004–06 and then decays (Spain:
  mean 48 in 2004–06 against 5.5 in 2018–25; Mexico peaks in 2006-04). Searches for the Spanish
  antivirus company Panda Security were most likely mapped into the topic in those years. This
  affects the level of the monthly `A_panda` in those years (use a break dummy if it is an outcome)
  and the Spanish scale factors, but no event in the 2011+ SPS series: the Spanish births are from
  2010 onward and the Mexican births predate Google's data.
* **Google collection changes** in 2016-01 and 2022-01 appear as small steps in several monthly series.
* **Single pulls.** Every Google series is a single pull (October 2026). Google Trends values are
  computed from a sample of searches and differ slightly between pulls.
* **Sparse regional data.** Sub-national daily data are mostly zeros outside large regions; regional
  windows are usable for fewer than half of the events (157 of 351).
* **Low-confidence announcement dates.** Japanese and Mexican announcements before 2011 are often
  copies of the birth date (`announce_confidence = low`). None of them is in the 2011+ SPS series.

## 9. Reproducing the dose from the daily file

```python
import pandas as pd
w = pd.read_csv("data/attention_daily_windows.csv")
w = w[(w.event_set == "panda_event") & (w.topic == "panda")]
post = w[w.rel_day.between(0, 2)].groupby("event_id").value_std.mean()
pre  = w[w.rel_day.between(-7, -3)].groupby("event_id").value_std.mean()
dose = post - pre          # equals events.csv dose_national
```
