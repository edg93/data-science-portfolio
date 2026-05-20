# Italian Tennis: One Half Rising, One Half Waiting

A data exploration of Italian tennis at the top of the ATP and WTA rankings since 2000 - and the contrast between the men's recent rise and the women's relative stagnation.

## The question

Italian tennis has had a remarkable few years on the men's tour. Jannik Sinner became the first Italian world #1 in singles. Lorenzo Musetti, Flavio Cobolli, and others have followed him into the top 20. Meanwhile on the women's tour, Jasmine Paolini stands almost alone at the top, with a notable gap behind her.

This project asks: **how does the data describe this asymmetry, and how is it different from the historical pattern?** A quick spoiler from the data - the historical pattern is actually the *reverse* of today's.

## Data source

All data is from [Jeff Sackmann's public tennis datasets](https://github.com/JeffSackmann):
- [`tennis_atp`](https://github.com/JeffSackmann/tennis_atp) — ATP (men's) ranking history and player metadata
- [`tennis_wta`](https://github.com/JeffSackmann/tennis_wta) — WTA (women's) ranking history and player metadata

These contain weekly ATP and WTA singles rankings from 2000 onwards, with player demographics (country, hand, height, date of birth). The data is curated and maintained by Jeff Sackmann.

## Structure

## Methodology notes

A few methodological choices worth documenting:

**Definition of "top Italian" each year.** The project defines the top Italian in a given year as the player who reached the highest peak ranking. As an alternative, the player with the most accumulated points that year was also computed - the two definitions agree in 50 of 54 year-gender combinations. The four differences (Volandri 2003, Starace 2010, Fognini 2019, Giorgi 2022) reflect years when a player had a higher single-tournament peak vs. a steadier season-long performance.

**Top N counts.** "How many Italians in the top N each year" counts each player once per year, based on whether their best ranking that year reached the threshold. Thresholds used: top 10, 50, 100, and 500. The 500 threshold captures the broader professional pipeline, not just the elite.

**Time window.** Analysis starts in 2000. Earlier data exists but the dataset's ranking history is more complete and consistent from 2000 onwards.

## Reproducing this analysis

The raw data is excluded from this repository (it's downloaded automatically by the preparation notebook). To reproduce:

1. Open `notebooks/data_preparation.ipynb`
2. Run all cells - it will download CSV files from Jeff Sackmann's GitHub repos into the `data/` folder
3. The notebook produces five derived CSV files used by the Tableau dashboard

## Tools used

- **Python** (pandas, pathlib) — data acquisition, cleaning, and aggregation
- **Tableau Public** — dashboard and visualisation *(coming)*
- **Jupyter Notebook** — data preparation environment

## Status

✅ Data preparation complete  
🔨 Tableau dashboard in progress  
⏳ Public dashboard link and screenshots to follow

## Headline findings (preview)

To be added once the dashboard is complete. The historical-vs-current contrast is the most interesting finding - Italian women's tennis has been historically stronger than the men's, with the relative position only inverting recently.
