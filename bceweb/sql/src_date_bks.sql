-- Date blocks (paged)
SELECT
   id,
   datime,
   tx_num,
   so_num,
   so_sum,
   lo_num,
   lo_sum,
   uo_num,
   uo_sum
FROM (
    SELECT * FROM bk
    WHERE DATE(datime) = '{date}'
) AS blocks
LEFT JOIN t_stat_bk ON t_stat_bk.b_id = blocks.id
ORDER BY id
OFFSET {offset} LIMIT {limit};