-- ======================================================
-- SQLZoo: SELECT within SELECT
-- https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial
-- ======================================================

-- 1. Countries with population larger than Russia's
SELECT name FROM world
WHERE population >
  (SELECT population FROM
    WHERE name = 'Russia');

-- 2. European countries with per-capita GDP greater than the UK's
SELECT name FROM world
WHERE gdp/population >
  (SELECT gdp/population FROM world
    WHERE name = 'United Kingdom')
AND continent = 'Europe';

-- 3. Countries in the same continent as Argentina or Australia, ordered by name
SELECT name, continent
FROM world
WHERE continent IN
  (SELECT continent FROM world
    WHERE name IN ('Argentina', 'Australia'))
ORDER BY name;

-- 4. Countries with population between the UK's and Germany's
SELECT name, population
FROM world
WHERE population >
  (SELECT population FROM world
    WHERE name = 'United Kingdom')
AND population <
  (SELECT population FROM world
    WHERE name = 'Germany');

-- 5. European countries: name and population as % of Germany's population
SELECT name, CONCAT(ROUND(100*population/
  (SELECT population FROM
    WHERE name = 'Germany')),'%') as 'percentage'
FROM world
WHERE continent = 'Europe';

-- 6. Countries with GDP greater than every country in Europe (ignore NULL GDPs)
SELECT name
FROM world
WHERE gdp > ALL(SELECT gdp
                FROM world
                WHERE gdp > 0
                AND continent = 'Europe');

-- 7. Largest country (by area) in each continent
SELECT continent, name, area FROM world x
WHERE area >= ALL
  (SELECT area FROM world y
    WHERE y.continent=x.continent
    AND area>0);

-- 8. Each continent and its alphabetically first country
SELECT continent, name
FROM world x
WHERE name <= ALL
  (SELECT name FROM world y
    WHERE y.continent = x.continent);

-- 9. Countries in continents where every country has population ≤ 25M
SELECT name, continent, population
FROM world
WHERE continent IN (
    SELECT continent
    FROM world
    GROUP BY continent
    HAVING MAX(population) <= 25000000
);

-- 10. Countries with population more than 3× that of every country in the same continent
SELECT name, continent
FROM world w1
WHERE w1.population > ALL (
    SELECT 3 * population
    FROM world w2
    WHERE w2.continent = w1.continent
      AND w2.name <> w1.name
);
