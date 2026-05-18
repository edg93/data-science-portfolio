-- ============================================
-- CO2 Emissions Exploratory Analysis
-- Dataset: Our World in Data CO2 emissions
-- Author: Enrico Di Gaspero
-- ============================================


-- Date range of the dataset
SELECT MIN(year), MAX(year)
FROM co2;

-- Number of countries
SELECT COUNT(DISTINCT country)
FROM co2;

-- top 10 countries by co2 emission in 2022
SELECT country, CAST(co2 AS REAL) as co2_emissions
FROM co2
WHERE year = 2022
AND iso_code != ''
ORDER BY co2_emissions DESC
LIMIT 10;

-- Italy co2 emissiones ordered
SELECT year, CAST(co2 AS REAL) as co2_emissions
FROM co2
WHERE country = 'Italy'
AND co2_emissions > 0
ORDER BY year;

-- Which country had the highest CO2 emissions in each decade:
SELECT
    (year/10)*10 as decade,
    country,
    MAX(CAST(co2 AS REAL)) as max_co2
FROM co2
WHERE iso_code != ''
GROUP BY decade
ORDER BY decade;

--Top 10 countries by cumulative CO2 emissions (all time):
SELECT
    country,
    CAST(cumulative_co2 AS REAL) as total_co2
FROM co2
WHERE year = 2022
AND iso_code != ''
ORDER BY total_co2 DESC
LIMIT 10;

-- CO2 per capita top 10 in 2022
SELECT country,
    CAST(co2_per_capita AS REAL) as co2_per_person
FROM co2
WHERE year = 2022
AND iso_code != ''
AND co2_per_capita != ''
ORDER BY co2_per_person DESC
LIMIT 10;

-- Total CO2 emissions by continent in 2022
-- (Note: 'iso_code' is empty for continents/regions in this dataset)
SELECT
    country as region,
    CAST(co2 AS REAL) as total_co2
FROM co2
WHERE year = 2022
AND country IN ('Europe', 'Asia', 'Africa', 'North America',
                'South America', 'Oceania')
ORDER BY total_co2 DESC;

-- Average CO2 per capita by decade (global)
SELECT
    (year/10)*10 as decade,
    ROUND(AVG(CAST(co2_per_capita AS REAL)), 2) as avg_co2_per_capita
FROM co2
WHERE iso_code != ''
AND co2_per_capita != ''
GROUP BY decade
ORDER BY decade;

-- Year-over-year CO2 growth for Italy
SELECT
    year,
    co2 as co2_emissions,
    LAG(co2) OVER (ORDER BY year) as previous_year,
    ROUND(
        co2 - LAG(co2) OVER (ORDER BY year))
        / LAG(co2) OVER (ORDER BY year) * 100,
        2
    ) as growth_pct
FROM co2
WHERE country = 'Italy'
AND year >= 1950
AND co2 != ''
ORDER BY year;

-- Top 3 emitters in each decade
WITH decade_emissions AS (
    SELECT
        (year/10)*10 as decade,
        country,
        SUM(co2) as decade_total_co2,
        RANK() OVER (
            PARTITION BY (year/10)*10
            ORDER BY SUM(co2) DESC
        ) as rnk
    FROM co2
    WHERE iso_code != ''
    AND co2 != ''
    AND year >= 1900
    GROUP BY decade, country
)
SELECT decade, country, ROUND(decade_total_co2, 0) as total_co2, rnk
FROM decade_emissions
WHERE rnk <= 3
ORDER BY decade, rnk;

-- Each country's share of global CO2 emissions in 2022
SELECT
    country,
    ROUND(co2, 0) as co2_emissions,
    ROUND(
        co2 * 100.0 / SUM(CAST(co2 AS REAL)) OVER (),
        2
    ) as pct_of_global
FROM co2
WHERE year = 2022
AND iso_code != ''
AND co2 != ''
ORDER BY co2_emissions DESC
LIMIT 15;

-- Cumulative CO2 emissions over time for top historical emitters
SELECT
    year,
    country,
    co2 as annual_co2,
    SUM(co2) OVER (
        PARTITION BY country
        ORDER BY year
    ) as cumulative_co2
FROM co2
WHERE country IN ('United States', 'China', 'Germany', 'United Kingdom')
AND year >= 1900
AND co2 != ''
ORDER BY country, year;
