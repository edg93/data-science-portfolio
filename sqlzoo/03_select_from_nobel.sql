-- ============================================
-- SQLZoo: SELECT from Nobel
-- https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial
-- ============================================

-- 1. Nobel prizes in 1950
SELECT yr, subject, winner
FROM nobel
WHERE yr = 1950;

-- 2. Winner of the 1962 prize for Literature
SELECT winner
FROM nobel
WHERE yr = 1962
AND subject = 'literature';

-- 3. Year and subject of Albert Einstein's prize
SELECT yr,subject FROM nobel
WHERE winner = 'Albert Einstein';

-- 4. Peace prize winners from 2000 onwards
SELECT winner FROM nobel
WHERE subject = 'peace'
AND yr >= 2000;

-- 5. Literature prize winners between 1980 and 1989 (inclusive)
SELECT yr,subject,winner FROM nobel
WHERE yr > 1979 AND yr < 1990
AND subject = 'literature';

-- 6. Prize details for presidential winners: T. Roosevelt, W. Wilson, J. Carter, B. Obama
SELECT * FROM nobel
WHERE winner IN ('Theodore Roosevelt', 'Thomas Woodrow Wilson', 'Jimmy Carter', 'Barack Obama');

-- 7. Winners with first name "John"
SELECT winner FROM nobel
WHERE winner LIKE 'John %';

-- 8. Physics winners in 1980 plus Chemistry winners in 1984
SELECT * FROM nobel
WHERE (subject = 'physics' AND yr = 1980)
OR (subject = 'chemistry' AND yr = 1984);

-- 9. 1980 winners, excluding Chemistry and Medicine
SELECT * FROM nobel
WHERE subject NOT IN ('chemistry', 'medicine')
AND yr = 1980;

-- 10. Medicine before 1910 (exclusive) and Literature from 2004 onwards (inclusive)
SELECT * FROM nobel
WHERE (subject = 'medicine' AND yr < 1910)
OR (subject = 'literature' AND yr >= 2004);

-- 11. Prize details for Peter Grünberg
SELECT * FROM nobel
WHERE winner = "Peter Grünberg";

-- 12. Prize details for Eugene O'Neill
SELECT * FROM nobel
WHERE winner = "eugene o\'neill";

-- 13. Winners starting with "Sir", ordered by year (recent first) then name
SELECT winner,yr,subject FROM nobel
WHERE winner LIKE 'Sir%'
ORDER BY yr DESC,winner;

-- 14. 1984 winners, ordered by subject (with Chemistry and Physics last) then by winner name
-- Trick: `subject IN (...)` returns 0/1 which works as a sort key.SELECT winner, subject
FROM nobel
WHERE yr = 1984
ORDER BY subject IN ('physics','chemistry'), subject, winner;
