# Outcome data: where to get them

The release contains no outcome data. Trade, tourism and bibliometric series are distributed by their
producers under their own terms, and users should download them directly. This file lists the sources
used in Yeh (2026), what to pull and how to merge the series with `data/panda_shocks_monthly.csv`
(keys `host` = ISO2, `month` = `YYYY-MM`). The paper's sample is 2000-01 to 2025-12, with mainland China
(ISO3 `CHN`, M49 `156`) as the partner.

## 1. Bilateral goods trade, monthly: IMF IMTS (formerly DOTS)

* **Dataset.** IMF *International Trade in Goods* (IMTS), the successor of the Direction of Trade
  Statistics (DOTS) on the 2025 IMF data portal.
* **Pull.** Reporter = each host (ISO3), indicators `XG_FOB_USD` (exports, FOB) and `MG_CIF_USD`
  (imports, CIF), counterparts `CHN` (mainland China) and `G001` (world), frequency `M`.
* **API (SDMX 3.0, no key).**
  `https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/IMTS/+/{ISO3+ISO3...}.XG_FOB_USD+MG_CIF_USD.CHN+G001.M?c[TIME_PERIOD]=ge:2000-M01`
  with header `Accept: application/vnd.sdmx.data+csv;version=2.0.0`. `OBS_VALUE` is in US dollars.
* **Taiwan** is not an IMF reporter. Use the Ministry of Finance trade database (query i9111,
  country-by-country trade values, general trade system).
* **Caveats.** Russia stopped publishing customs data in 2022, so IMF figures from 2022-01 are
  estimates. Hong Kong's exports to the mainland include re-exports. Taiwan's trade before 2002 went
  largely through Hong Kong.

## 2. Trade by product (HS 2-digit), monthly

* **UN Comtrade.** `https://comtradeapi.un.org/public/v1/preview/C/M/HS?reporterCode=..&period=YYYYMM&partnerCode=156`
  (free preview endpoint; a free API key raises the limits). Pull HS chapters 01–99, flows M and X,
  partner 156 (China) and 0 (world).
* **Eurostat Comext** for the EU hosts (AT BE DE DK ES FI FR NL): dataset `DS-045409` (EU trade since
  1988 by HS2–4–6 and CN8), monthly, partner `CN`, via
  `https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409?format=JSON&freq=M`.
  Comext also gives the other extra-EU origins, which a triple-difference design needs.
* **Grouping.** Consumer, intermediate and capital goods can be defined with the BEC classification
  (UN Statistics Division correspondence tables).

## 3. Chinese visitors in the host, monthly

**Eurostat.** `tour_occ_nim` (nights) and `tour_occ_arm` (arrivals) report only domestic, foreign and
total residents, so a query with `c_resid=CN` returns an empty dataset. The China split exists:

* monthly from 2005 to 2011 in the discontinued `tour_occ_ninrmw` and `tour_occ_arnrmw` (the
  Netherlands not reported);
* annually from 1990 to date in `tour_occ_ninraw` and `tour_occ_arnraw` (use these as a cross-check).

After 2011 the EU hosts need national statistics. The paper uses these sources:

| host | source | series |
|---|---|---|
| US | NTTO (trade.gov), I-94 monthly arrivals | residence PRC, overseas visitors |
| CA | Statistics Canada table 24-10-0050-01 | non-resident visitors, residence China |
| AU | ABS Data API `OAD_COUNTRY` | short-term visitor arrivals, residence China; also short-term resident returns from China |
| JP | JNTO visitor arrivals | nationality China |
| KR | Korea Tourism Organization (know.tour.go.kr) | nationality China |
| SG | SingStat Table Builder M550001 | residence mainland China |
| HK | C&SD table 650-80001 | mainland visitors, overnight + same-day |
| MO | DSEC, indicator 14042 | mainland visitors |
| MY | Tourism Malaysia, then data.gov.my (Immigration) | arrivals CHN |
| TH | Ministry of Tourism and Sports, monthly files | nationality China |
| ID | BPS / Kemenpar | arrivals "Tiongkok" (2022+) |
| MX | SEGOB/UPM Boletín estadístico, table 1.3 | air entries of Chinese nationals |
| TW | Tourism Administration (stat.taiwan.net.tw) | visitor arrivals by residence, mainland China |
| AT | Statistik Austria OGD `OGD_touextsai_Tour_HKL_1` | nights, China |
| DK | Statistics Denmark StatBank `TURIST` | nights, nationality China |
| FI | Statistics Finland `StatFin/matk/11iz.px` | nights, residence China |
| NL | CBS StatLine 70022ned (to 2011), 82061NED (2012+, hotels only) | nights, China |
| ES | INE experimental mobile-phone statistic (2019-07+) | nights, China residents |
| GB | ONS International Passenger Survey (quarterly only) | visits and nights, China |

DE, BE and FR publish no monthly series of Chinese visitors after 2011, and QA no China split at all.
Mark 2020-02 to 2023-01 (China's outbound travel closure) as a separate regime. `data/policy_regimes.csv`
gives the dated tour bans, visa waivers and flight suspensions.

## 4. Scientific co-authorship: OpenAlex

* **API.** `https://api.openalex.org/works` (free; an API key raises the daily budget).
* **Pull.** One request per month and series with `group_by=authorships.countries` and `per_page=200`:
  * `filter=type:article,institutions.country_code:CN,publication_date:YYYY-MM-01..YYYY-MM-last` gives,
    for each country, the number of works that have at least one author in that country and one in China;
  * the same request without the CN filter gives each host's total output.
  * Field versions add `concepts.id` (for example Biology `C86803240`).
* **Outcomes.** Log host–China co-authored works, and the China share of host output.

## 5. Merging and controls

```python
import pandas as pd
z = pd.read_csv("data/panda_shocks_monthly.csv")
y = pd.read_csv("my_outcome.csv")          # columns host, month (YYYY-MM), y
df = z.merge(y, on=["host", "month"], how="left")
```

The paper's controls are the exchange rate against the renminbi, the country geopolitical-risk index
of Caldara and Iacoviello (2022), the country economic-policy-uncertainty index of Baker, Bloom and
Davis (2016), the change in China's OECD composite leading indicator, and host total exports. All are
public; download them from the producers.
