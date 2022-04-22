SELECT DISTINCT
  tx.id AS id,
  b_id,
  datime,
  hash,
  (SELECT COUNT(*) FROM vout WHERE t_id_in = 10000000) AS vi_num,
  (SELECT COUNT(*) FROM vout WHERE t_id = 10000000) AS vo_num
FROM tx
INNER JOIN bk ON bk.id = tx.b_id
WHERE tx.id = {tx};
