SELECT
    dates.d AS date,
    bk_num,
    lo_num,
    lo_sum,
    so_num,
    so_sum,
    uo_num,
    uo_sum
FROM (
    SELECT
        DATE(datime) AS d,
        COUNT(*) AS bk_num
    FROM bk
    WHERE
        EXTRACT (YEAR FROM datime) = {year}
        AND EXTRACT (MONTH FROM datime) = {month}
    GROUP BY d
) AS dates
LEFT JOIN t_stat_date ON t_stat_date.d = dates.d
ORDER BY date;
