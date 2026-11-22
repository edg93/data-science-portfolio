# Climate Change in Friuli Venezia Giulia: 35 Years of Weather Data

A data analysis project examining long-term weather trends in Friuli Venezia Giulia, Italy, using historical observations from the regional meteorological network (OSMER) since 1991.

## The question

Has the climate in Friuli Venezia Giulia measurably changed over the last 35 years? The region's diverse geography — Adriatic coast, Friulian plains, pre-Alps and Alps all within ~100 km — makes it a particularly interesting place to look for climate signals: different environments should show different patterns of change.

This project asks: **what do the data show about how temperature, rainfall, and extremes have evolved in the region since 1993?**

## Data source

Daily weather observations from [ARPA FVG - OSMER e GRN](http://www.meteo.fvg.it/), the regional meteorological observatory of Friuli Venezia Giulia, accessed via the [public archive](https://www.osmer.fvg.it/archivio.php?ln=&p=dati).

Data released under [CC BY-SA 3.0 IT](http://creativecommons.org/licenses/by-sa/3.0/it/).
Any derived data redistributed from this project inherits the same license.

### Variables (daily)

- Rainfall (mm)
- Temperature: min / mean / max (°C)
- Humidity: min / mean / max (%)
- Wind: mean speed / gust max (km/h) + gust direction
- Solar radiation (KJ/m²)
- Atmospheric pressure (hPa)

## Structure

```
climate-fvg/
├── README.md
├── scripts/
│   └── scrape_osmer.py       ← pulls data from the OSMER archive
├── data/
│   ├── stations.csv          ← station metadata
│   ├── raw/                  ← one CSV per (station, year) — gitignored
│   └── processed/            ← cleaned, filtered daily data — gitignored
└── notebooks/
    └── climate_analysis.ipynb   ← cleaning + analysis
```

## Stations

Fifteen stations selected for their long continuous records and geographic diversity, covering an elevation gradient of 0 m to 1750 m from the Adriatic coast to the Julian Alps:

| Station | Role | Elevation |
|---|---|---|
| Fossalon | Coastal plain | 0 m |
| Trieste (Molo Fratelli Bandiera) | Coast (Bora exposure) | 1 m |
| Palazzolo dello Stella | Coastal lagoon | 5 m |
| Talmassons | Southern plain | 16 m |
| San Vito al Tagliamento | Western plain | 21 m |
| Brugnera | Pordenone plain | 22 m |
| Gradisca d'Isonzo | Isonzo plain | 29 m |
| Capriva del Friuli | Collio | 85 m |
| Udine S.O. | Central plain | 91 m |
| Vivaro | Pordenone foothills | 142 m |
| Fagagna | Udine foothills | 148 m |
| Enemonzo | Carnia foothills | 438 m |
| Tarvisio | Alpine valley | 794 m |
| Monte Lussari | High Julian Alps | 1743 m |
| Monte Zoncolan | High Carnian Alps | 1750 m |

## Methodology notes

A few decisions worth documenting:

**Time window.** 1993–2024 (32 years). Before 1993 only a handful of stations were reporting; after 2024 the recent-data validation at OSMER is incomplete.

**Old/new station merges.** Several stations in the OSMER archive appear as "old" and "new" entries at identical coordinates (e.g. `Ariis_old` / `Ariis`, `Pontebba_old` / `Pontebba`). These represent equipment replacements at the same physical location and are merged into single continuous records. Overlap days (where both installations reported on the same date) are resolved by keeping the row with more non-null observations. Monte Lussari is a borderline case (~17 m vertical offset between old and new) — merged for continuity, but the warming trend at this station should be interpreted with awareness that small instrument calibration differences could inflate it.

**A data-quality artifact.** Inspection revealed that for Fossalon and Monte Zoncolan in 1993 and 1994, the `temp_mean` column exactly matches the `temp_max` column, producing implausibly warm annual means at those stations. A systematic check confirmed this is isolated to those four station-years. We null out the affected `temp_mean` cells; other columns (`temp_min`, `temp_max`, rainfall, humidity, wind, etc.) remain usable.

## Reproducing this analysis

The raw data is excluded from this repository. To reproduce:

1. Run `scripts/scrape_osmer.py` — downloads one CSV per (station, year) into `data/raw/` and writes station metadata to `data/stations.csv`. Takes ~90 minutes at 2 seconds per request.
2. Open `notebooks/climate_analysis.ipynb` and run all cells. Part 1 assembles the processed dataset; Part 2 performs the analysis.

## Status

🔨 **In progress.**

- ✅ Scraper: pulls 63 stations, 1991–2026, ~707k daily observations
- ✅ Data preparation: merged, cleaned, filtered to 15 stations × 32 years = ~171k rows
- ✅ Section 2.1: Temperature trends
- ⏳ Section 2.2: Extreme heat days
- ⏳ Section 2.3: Frost and cold snaps
- ⏳ Section 2.4: Rainfall patterns
- ⏳ Section 2.5: Elevation gradient
- ⏳ Section 2.6: Conclusion

## Preliminary findings (temperature)

**The region has warmed by about 1.3 °C since 1993.**

- Regional annual mean has risen at **+0.41 °C per decade** (R² = 0.36, p < 0.001) — matching the Italian national average and above the global mean rate.
- All 15 stations show statistically significant warming. Rates range from +0.37 to +1.09 °C per decade.
- The Friulian plain warms fastest, consistently at +0.5–0.9 °C/decade.
- Tarvisio (Alpine valley, 794 m) is the slowest-warming at +0.37 °C/decade, consistent with other European Alpine valleys where cold-air pooling dampens temperature trends.
- 2024 was the warmest year on
