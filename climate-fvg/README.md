# Climate Change in Friuli Venezia Giulia: 35 Years of Weather Data

A data analysis project examining long-term weather trends in Friuli Venezia
Giulia, Italy, using historical observations from the regional meteorological
network (OSMER) since 1991.

## The question

Has the climate in Friuli Venezia Giulia measurably changed over the last 35
years?

This project asks: **what do the data show about how temperature, rainfall,
and extremes have evolved in the region since 1991?**

## Data source

Daily weather observations from [ARPA FVG - OSMER e GRN](http://www.meteo.fvg.it/),
the regional meteorological observatory of Friuli Venezia Giulia, accessed via
the [public archive](https://www.osmer.fvg.it/archivio.php?ln=&p=dati).

Data released under [CC BY-SA 3.0 IT](http://creativecommons.org/licenses/by-sa/3.0/it/).
Any derived data redistributed from this project inherits the same license.

### Variables available (daily)

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
│   ├── raw/                  ← one CSV per (station, year) — gitignored
│   └── processed/            ← cleaned, combined data — gitignored
└── notebooks/
    └── (coming)              ← cleaning + analysis
```

## Stations (planned)


## Reproducing this analysis

The raw data is excluded from this repository (downloaded locally by the
scraper). To reproduce:

1. Run `scripts/scrape_osmer.py` to download CSVs into `data/raw/`
2. Open the notebooks in `notebooks/` to clean and analyse

The scraper respects OSMER's servers with a 2.5s delay between requests.
Running the full set (~8 stations × 35 years = ~15 minutes).

## Attribution

Data courtesy of **ARPA FVG - OSMER e GRN**, http://www.meteo.fvg.it/,
licensed under CC BY-SA 3.0 IT. The data has been modified: aggregated,
filtered, and transformed for this analysis.

## Tools used

- **Python** (pandas, requests, BeautifulSoup) — scraping, cleaning, analysis
- **Jupyter Notebook** — analytical environment
- **scipy / matplotlib / seaborn** — statistics and visualisation

## Status

🔨 **In progress** — scraper built, data download underway. Analysis to follow.
