-- ============================================
-- SQLZoo: SELECT from World
-- https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial
-- ============================================

-- (Problem 1 is the introductory example.)

-- 2. Show countries with population greater than 200M
SELECT name FROM world
WHERE population >= 200000000;

-- 3. Show per-capita GDP of countries with population >= 200M
SELECT name,GDP/population AS "per capita GDP" FROM world
WHERE population > 200000000;

-- 4. Name and population (in millions) for South American countries
SELECT name,population/1000000 AS 'Population in millions' FROM world
WHERE continent = 'South America';

-- 5. Name and population for France, Germany, Italy
SELECT name,population
FROM world
WHERE name IN ('France','Germany','Italy');

-- 6. Countries whose name contains "United"
SELECT name FROM world
WHERE name LIKE '%United%';

-- 7. Big by area (>3M km²) OR big by population (>250M): name, population, area
SELECT name,population,area FROM world
WHERE population >250000000 OR area > 3000000;

-- 8. Big by area XOR big by population (one but not both): name, population, area
SELECT name,population,area FROM world
WHERE population >250000000 XOR area > 3000000;

-- 9. Americas: name, population (millions) and GDP (billions), both to 2 dp
SELECT name,
       ROUND(population / 1000000, 2)   AS population_millions,
       ROUND(gdp / 1000000000, 2)       AS gdp_billions
FROM world
WHERE continent = 'South America';;

-- 10. Per-capita GDP rounded to nearest $1000 for trillion-dollar economies
SELECT name,round(GDP/population,-3) AS 'GDP per capita'
FROM world
WHERE GDP >= 1000000000000;

-- 11. Countries where name and capital have the same length
SELECT name,capital
FROM world
WHERE LENGTH(name) = LENGTH(capital);

-- 12. Countries where name and capital share their first letter (and differ)
SELECT name, capital
FROM world
WHERE LEFT(name,1) = LEFT(capital,1) AND name<>capital;

-- 13. Single-word country name containing all five vowels
SELECT name
FROM world
WHERE name LIKE '%e%'
AND name LIKE '%a%'
AND name LIKE '%i%'
AND name LIKE '%o%'
AND name LIKE '%u%'
AND name NOT LIKE '% %';
