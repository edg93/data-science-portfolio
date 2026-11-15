"""
OSMER FVG Archive Scraper
Downloads daily weather data from https://www.osmer.fvg.it/archivio.php
Respects CC BY-SA 3.0 IT license (attribution to ARPA FVG - OSMER e GRN).
"""

import requests
import pandas as pd
from pathlib import Path
import time
import io
import json

# ============================================
# Configuration
# ============================================

ENDPOINT = "https://www.osmer.fvg.it/ajax/getStationData.php"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.osmer.fvg.it/archivio.php?ln=&p=dati",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.osmer.fvg.it",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

COOKIES = {"meteofvg_cookie": "1"}

# Polite delay between requests
DELAY_SECONDS = 2.5

# Output folder (relative to scripts/)
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"

# ============================================
# Stations to scrape
# ============================================
# Format: "CODE@Name@type@lat@lon@elevation"
# We'll add more after we get the full list from the archive dropdown.

STATIONS = {
    "Udine": "UDI@Udine S.O.@syn@46.035212@13.226672@91",
}

YEARS = range(1991, 2027)   # 1991 through 2026


# ============================================
# Core functions
# ============================================

def fetch_station_year(station_id: str, year: int) -> pd.DataFrame | None:
    """
    Fetch one (station, year) of daily data and return it as a DataFrame.
    Returns None if the response contains no real data (all dashes).
    """
    payload = {
        "a": str(year),
        "m": "99",      # all months
        "g": "99",      # all days
        "s": station_id,
        "t": "H_3",     # daily data
        "ln": "",
        "o": "visualizza",
    }

    response = requests.post(
        ENDPOINT,
        headers=HEADERS,
        cookies=COOKIES,
        data=payload,
        timeout=30,
    )
    response.raise_for_status()

    # Response is JSON-encoded HTML string
    html = response.json() if response.text.startswith('"') else response.text

    # pandas can parse HTML tables directly
    tables = pd.read_html(io.StringIO(html))
    if not tables:
        return None

    df = tables[0]

    # Check if the data is all dashes (station wasn't reporting that year)
    data_cols = [c for c in df.columns if c not in ("mese", "giorno")]
    if df[data_cols].astype(str).eq("-").all().all():
        return None

    return df


def scrape_all(stations: dict, years) -> None:
    """Loop through stations × years, save one CSV per combination."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    total = len(stations) * len(list(years))
    done = 0

    for station_name, station_id in stations.items():
        for year in years:
            done += 1
            out_path = RAW_DIR / f"{station_name}_{year}.csv"

            if out_path.exists():
                print(f"[{done}/{total}] skip (exists): {out_path.name}")
                continue

            try:
                df = fetch_station_year(station_id, year)
            except Exception as e:
                print(f"[{done}/{total}] ERROR {station_name} {year}: {e}")
                time.sleep(DELAY_SECONDS)
                continue

            if df is None:
                print(f"[{done}/{total}] {station_name} {year}: no data (skipped)")
            else:
                df.to_csv(out_path, index=False)
                print(f"[{done}/{total}] saved {out_path.name} ({len(df)} rows)")

            time.sleep(DELAY_SECONDS)


# ============================================
# Entry point
# ============================================

if __name__ == "__main__":
    scrape_all(STATIONS, YEARS)
    print("\nDone.")