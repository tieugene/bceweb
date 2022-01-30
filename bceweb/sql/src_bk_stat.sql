SELECT DISTINCT
  bk.*,
  t_bk_stat.*
FROM bk
LEFT JOIN t_bk_stat ON bk.id = t_bk_stat.b_id
WHERE id = {bk};
