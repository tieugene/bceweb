-- Dates of month data
SELECT *
FROM (
    SELECT
        DATE(datime) AS date,
        COUNT(*) AS bk_num,
        MAX(id) AS bk_max
    FROM bk
    WHERE
        EXTRACT (YEAR FROM datime) = {year}
        AND EXTRACT (MONTH FROM datime) = {month}
    GROUP BY d
) AS m
LEFT JOIN t_stat_date ON t_stat_date.d = m.date
ORDER BY date;
