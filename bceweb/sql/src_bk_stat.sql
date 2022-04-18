-- block data with cumulatives
SELECT DISTINCT *
FROM bk
LEFT JOIN t_stat_bk ON bk.id = t_stat_bk.b_id
WHERE id = {bk};
