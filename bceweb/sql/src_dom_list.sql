-- Dates of month data
SELECT
    m.d AS date,
    bk_num, bk_max,
    so_num, so_sum,
    lo_num, lo_sum,
    uo_num, uo_sum,
    so_num_inc, so_sum_inc,
    lo_num_inc, lo_sum_inc,
    uo_num_inc, uo_sum_inc
FROM (
    SELECT
        DATE(datime) AS d,
        COUNT(*) AS bk_num,
        MAX(id) AS bk_max
    FROM bk
    WHERE
        EXTRACT (YEAR FROM datime) = {year}
        AND EXTRACT (MONTH FROM datime) = {month}
    GROUP BY d
) AS m
LEFT JOIN (
    SELECT
        *,
        SUM(so_num) OVER (ORDER BY d) AS so_num_inc,
        SUM(so_sum) OVER (ORDER BY d) AS so_sum_inc,
        SUM(lo_num) OVER (ORDER BY d) AS lo_num_inc,
        SUM(lo_sum) OVER (ORDER BY d) AS lo_sum_inc,
        SUM(uo_num) OVER (ORDER BY d) AS uo_num_inc,
        SUM(uo_sum) OVER (ORDER BY d) AS uo_sum_inc
    FROM
        t_stat_date
) AS s ON s.d = m.d
ORDER BY date;
