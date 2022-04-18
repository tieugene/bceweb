-- Date blocks (paged)
SELECT
   id,
   datime,
   tx_num,
   so_num, so_sum,
   lo_num, lo_sum,
   uo_num, uo_sum,
   tx_num_inc,
   so_num_inc, so_sum_inc,
   lo_num_inc, lo_sum_inc,
   uo_num_inc, uo_sum_inc
FROM (
    SELECT * FROM bk
    WHERE DATE(datime) = '{date}'
) AS m
LEFT JOIN (
    SELECT
        *,
        SUM(tx_num) OVER (ORDER BY b_id) AS tx_num_inc,
        SUM(so_num) OVER (ORDER BY b_id) AS so_num_inc,
        SUM(so_sum) OVER (ORDER BY b_id) AS so_sum_inc,
        SUM(lo_num) OVER (ORDER BY b_id) AS lo_num_inc,
        SUM(lo_sum) OVER (ORDER BY b_id) AS lo_sum_inc,
        SUM(uo_num) OVER (ORDER BY b_id) AS uo_num_inc,
        SUM(uo_sum) OVER (ORDER BY b_id) AS uo_sum_inc
    FROM
        t_stat_bk
) AS s ON s.b_id = m.id
ORDER BY id
OFFSET {offset} LIMIT {limit};