SELECT DISTINCT
    DATE(datime) AS date,
    COUNT(*) AS num
FROM bk
GROUP BY date
ORDER BY date
OFFSET {offset} LIMIT {limit};