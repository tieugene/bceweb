SELECT
    MAX(EXTRACT (DAY FROM datime))
FROM bk
WHERE
    EXTRACT (YEAR FROM datime) = {year} AND
    EXTRACT (MONTH FROM datime) = {month};