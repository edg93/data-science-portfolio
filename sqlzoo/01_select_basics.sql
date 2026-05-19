-- ============================================
-- SQLZoo: SELECT basics
-- https://sqlzoo.net/wiki/SELECT_basics
-- ============================================

-- 1. Show the population of Germany
SELECT population FROM world
WHERE name = 'Germany';

-- 2. Show name and population for Sweden, Norway and Denmark
SELECT name, population FROM world
WHERE name IN ('Sweden', 'Norway', 'Denmark');

-- 3. Show countries with area between 200k and 250k
SELECT name, area FROM world
WHERE area BETWEEN 200000 AND 250000;
