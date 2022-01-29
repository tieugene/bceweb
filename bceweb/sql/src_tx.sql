SELECT DISTINCT
  id,
  b_id,
  hash,
  (SELECT COUNT(*) FROM vout WHERE t_id_in = {tx}) AS vi_num,
  (SELECT COUNT(*) FROM vout WHERE t_id = {tx}) AS vo_num
FROM tx
WHERE id = {tx};