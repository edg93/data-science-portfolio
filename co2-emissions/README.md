# CO2 Emissions Analysis: Has the Paris Agreement Changed Anything?

Analysis of global CO2 emissions before and after the Paris Agreement (2015), using SQL and Python.

## The question

The Paris Agreement, signed in December 2015, saw nearly every country commit to limiting warming to well below 2°C. Almost a decade later, has anything actually changed in the emissions data?

## Structure

- `sql/queries.sql` — exploratory SQL queries against the dataset
- `notebooks/paris_agreement_analysis.ipynb` — main analysis and visualisations
- `data/` — SQLite database and raw CSVs (excluded from git, see below)

## Data source

This analysis uses the [Our World in Data CO2 and Greenhouse Gas Emissions](https://ourworldindata.org/co2-and-greenhouse-gas-emissions) dataset.

- **Authors:** Pablo Rosado, Hannah Ritchie, Max Roser, Edouard Mathieu, Bobbie Macdonald
- **License:** Creative Commons BY

## Reproducing this analysis

The SQLite database and raw CSV files are excluded from git due to size. To reproduce:

1. Download `owid-co2-data.csv` from the [OWID repository](https://github.com/owid/co2-data)
2. Load it into a SQLite database named `CO2_emissions.db` and place it in `data/`
3. Open the notebook in `notebooks/` and run all cells

## Tools used

- **SQL** (SQLite) — exploration, aggregations, window functions, CTEs
- **Python** (pandas, matplotlib, seaborn) — analysis and visualisation

## Key findings

**At the global level**, emissions in 2024 are about 6% below where the 1990–2014 linear trajectory would have placed them - a real but modest deviation. However, growth had already started moderating before Paris was signed, so much of this gap reflects pre-existing structural shifts, not a Paris-triggered break.

**Country trajectories vary enormously.** Between the pre-Paris (2010–2014) and post-Paris (2018–2022) windows:
- The UK cut emissions 28% — the deepest cut in the sample
- Italy, Japan and the EU-27 each cut 13–17%
- The US cut 8%, Brazil 4%, Russia stayed flat
- China grew 15% and India 38%

**Carbon leakage is real but uneven.** The UK and US show the textbook pattern (production-based cuts partly offset by imports), but Italy, Japan, Brazil and Russia show the *opposite* — their consumption fell more than their production. The "OECD just outsourced its emissions" critique is partly true, partly misleading.

**Most inflection points are not at 2015.** The UK's steep decline accelerated in 2012. The US peaked around 2007 (shale gas displacing coal). The EU has been declining since 2007. The countries that bent their curves mostly did so based on pre-existing structural shifts - domestic energy policy, coal phase-outs, renewables scaling — not the Paris Agreement itself.

**The honest conclusion:** the world has slowly bent the emissions curve since the early 2010s, with Paris as one milestone in a longer process rather than the cause of it. National-level energy infrastructure decisions appear to matter more than international agreements.
