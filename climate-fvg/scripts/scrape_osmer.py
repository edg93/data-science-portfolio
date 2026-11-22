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
DELAY_SECONDS = 2

# Output folders (relative to scripts/)
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

# ============================================
# Stations to scrape
# ============================================
# Format: "CODE@Name@type@lat@lon@elevation"

STATIONS = {
    "Ariis_old":        "ARIIS-ETPI@Ariis (fino al 03/05/2024)@syn@45.878300@13.090000@13",
    "Ariis":            "ARI@Ariis@syn@45.878300@13.090000@13",
    "Barcis_old":       "BAR@Barcis (fino al 18/02/2021)@syn@46.193202@12.571028@468",
    "Barcis":           "103400@Barcis@syn@46.193202@12.571028@468",
    "Bicinicco":        "BIC@Bicinicco@syn@45.928808@13.240140@33",
    "BoaPaloma":        "BOA@Boa Paloma (interruzione dati dal 06/02/2018 al 29/06/2022)@syn@45.618291@13.565022@5",
    "Bordano":          "BOR@Bordano (fino al 21/04/2021)@syn@46.332764@13.081196@230",
    "Brugnera":         "BRU@Brugnera@syn@45.917972@12.545003@22",
    "Capriva":          "CAP@Capriva del Friuli@syn@45.958094@13.512333@85",
    "CaveDelPredil":    "CDP@Cave del Predil@syn@46.437067@13.567703@914",
    "Cervignano":       "CER@Cervignano del Friuli@syn@45.849486@13.337015@8",
    "Chievolis":        "CHI@Chievolis@syn@46.254523@12.734044@345",
    "Cividale":         "CIV@Cividale del Friuli@syn@46.080442@13.420014@127",
    "Codroipo":         "COD@Codroipo@syn@45.952356@13.002742@37",
    "Enemonzo":         "ENE@Enemonzo@syn@46.410416@12.862536@438",
    "Faedis":           "FAE@Faedis (fino al 19/06/2019)@syn@46.134532@13.352326@158",
    "Fagagna":          "FAG@Fagagna@syn@46.101692@13.073886@148",
    "ForniDiSopra":     "FSP@Forni di Sopra@syn@46.409798@12.593680@922",
    "Fossalon":         "FOS@Fossalon@syn@45.714768@13.458865@0",
    "Gemona":           "GEM@Gemona del Friuli@syn@46.261297@13.122088@184",
    "Gorgo":            "GRG@Gorgo@syn@45.736227@13.021904@5",
    "GoriziaAeroporto": "142300@Gorizia Aeroporto@syn@45.91039@13.595497@68",
    "Gradisca":         "GRA@Gradisca d'Is.@syn@45.889791@13.481807@29",
    "Grado_old":        "GRD@Grado (fino al 12/09/2019)@syn@45.676400@13.394500@5",
    "GradoMare_old":    "GRM@Grado-mare (fino al 19/08/2021)@syn@45.671362@13.396556@0",
    "GradoMeteo":       "178200@Grado Meteo@syn@45.68035@13.373289@0",
    "GradoMarea":       "188100@Grado Marea@syn@45.683158@13.383429@0",
    "Lauzacco":         "LAU@Lauzacco@syn@45.982046@13.272538@60",
    "Lignano_old":      "LIG@Lignano@syn@45.701909@13.147078@7",
    "LignanoSabbiadoro":"343800@Lignano Sabbiadoro@syn@45.701909@13.147078@7",
    "MickeyZegla":      "Zegla-ARPA@Mickey Zegla@syn@45.969832@13.513413@53",
    "Monfalcone_old":   "MNF@Monfalcone (fino al 23/04/2021)@syn@45.780471@13.536554@0",
    "Monfalcone":       "343400@Monfalcone@syn@45.780471@13.536554@0",
    "MonfalconePluvio": "501000@Monfalcone Pluvio@syn@45.780471@13.536554@0",
    "MonteLussari_old": "LUS@Monte Lussari (fino al 08/01/2018)@syn@46.482473@13.520457@1760",
    "MonteLussari":     "LSR@Monte Lussari@syn@46.482536@13.520058@1743",
    "MonteMatajur":     "MAT@Monte Matajur@syn@46.211683@13.529107@1630",
    "MonteZoncolan":    "ZON@Monte Zoncolan@syn@46.502355@12.926251@1750",
    "Muggia":           "MGG@Muggia@syn@45.610495@13.752682@2",
    "MuggiaPluvio":     "344200@Muggia Pluvio@syn@45.610495@13.752682@2",
    "Musi":             "MUS@Musi@syn@46.312663@13.274682@600",
    "PalaDAltei":       "PDA@Pala d'Altei@syn@46.157287@12.597723@1528",
    "PalazzoloStella":  "PAL@Palazzolo dello Stella@syn@45.805702@13.052598@5",
    "Piancavallo":      "PIA@Piancavallo@syn@46.114922@12.524386@1275",
    "Pontebba_old":     "PNT@Pontebba (fino al 14/09/2017)@syn@46.509586@13.302481@590",
    "Pontebba":         "213200@Pontebba@syn@46.509586@13.302481@590",
    "Pordenone_old":    "POR@Pordenone (fino al 31/03/2025)@syn@45.953618@12.681257@23",
    "PordenoneMeteo":   "342600@Pordenone Meteo@syn@45.953618@12.681257@23",
    "Pradamano":        "PRD@Pradamano@syn@46.044247@13.303041@91",
    "SSimeoneMeteo":    "499900@S. Simeone Meteo@syn@46.343737@13.105049@1504",
    "SanPietro":        "SPN@San Pietro al Natisone@syn@46.114260@13.486796@160",
    "SanVito":          "SAN@San Vito al Tgl.@syn@45.895661@12.814989@21",
    "Sappada":          "SAP@Sappada (ARPAV)@syn@46.5700@12.7083@1265",
    "Sgonico":          "SGO@Sgonico-Zgonik@syn@45.738004@13.742056@268",
    "Talmassons":       "TAL@Talmassons@syn@45.882311@13.155779@16",
    "Tarvisio":         "TAR@Tarvisio@syn@46.510775@13.551886@794",
    "Tolmezzo_old":     "TOL@Tolmezzo (fino al 11/11/2025)@syn@46.399425@13.005854@314",
    "TolmezzoMeteo":    "343700@Tolmezzo Meteo@syn@46.421844@13.021877@314",
    "TriesteNautico":   "TRS@Trieste Ist. Nautico@syn@45.647393@13.764540@30",
    "Trieste":          "TRI@Trieste molo F.lli Bandiera@syn@45.649996@13.752242@1",
    "TriesteCattinara": "343200@Trieste Cattinara@syn@45.635432@13.833167@257",
    "Udine":            "UDI@Udine S.O.@syn@46.035212@13.226672@91",
    "Vivaro":           "VIV@Vivaro@syn@46.076529@12.768814@142",
}

YEARS = range(1991, 2027)   # 1991 through 2026


# ============================================
# Core functions
# ============================================

def save_station_metadata(stations: dict, out_path: Path) -> None:
    """
    Parse the "code@name@type@lat@lon@elevation" station strings into a 
    clean CSV lookup table for use in analysis.
    """
    rows = []
    for key, s in stations.items():
        parts = s.split("@")
        if len(parts) >= 6:
            rows.append({
                "key": key,
                "code": parts[0],
                "name_full": parts[1],
                "type": parts[2],
                "lat": float(parts[3]),
                "lon": float(parts[4]),
                "elevation_m": int(parts[5]),
            })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"Saved station metadata: {out_path} ({len(rows)} stations)")


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

    # Always refresh station metadata — cheap and keeps analysis in sync
    save_station_metadata(stations, DATA_DIR / "stations.csv")

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