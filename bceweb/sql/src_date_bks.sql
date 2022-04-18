-- Date blocks (paged)
SELECT *
FROM (
    SELECT * FROM bk
    WHERE DATE(datime) = '{date}'
) AS m
LEFT JOIN t_stat_bk ON t_stat_bk.b_id = m.id
ORDER BY id
OFFSET {offset} LIMIT {limit};
