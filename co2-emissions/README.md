# CO2 Emissions Analysis: Has the Paris Agreement Changed Anything?

Analysis of global CO2 emissions before and after the Paris Agreement (2015),
using SQL and Python.

## The question

The Paris Agreement, signed in December 2015, saw nearly every country commit
to limiting warming to well below 2°C. Almost a decade later, has anything
actually changed in the emissions data?

## Structure

- `sql/queries.sql` — exploratory SQL queries against the dataset
- `notebooks/paris_agreement_analysis.ipynb` — main analysis and visualisations
- `data/` — SQLite database and raw CSVs (excluded from git, see below)

## Data source

This analysis uses the [Our World in Data CO2 and Greenhouse Gas Emissions](https://ourworldindata.org/co2-and-greenhouse-gas-emissions) dataset.

- **Authors:** Pablo Rosado, Hannah Ritchie, Max Roser, Edouard Mathieu, Bobbie Macdonald
- **License:** Creative Commons BY

## Reproducing this analysis

The SQLite database and raw CSV files are excluded from git due to size. To
reproduce:

1. Download `owid-co2-data.csv` from the [OWID repository](https://github.com/owid/co2-data)
2. Load it into a SQLite database named `CO2_emissions.db` and place it in `data/`
3. Open the notebook in `notebooks/` and run all cells

## Tools used

- **SQL** (SQLite) — exploration, aggregations, window functions, CTEs
- **Python** (pandas, matplotlib, seaborn) — analysis and visualisation

## Key findings

To be added once analysis is complete.
