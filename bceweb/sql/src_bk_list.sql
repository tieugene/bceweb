SELECT *
FROM bk
LEFT JOIN t_stat_bk ON bk.id = t_stat_bk.b_id
ORDER BY bk.id
OFFSET {offset} LIMIT {limit};
