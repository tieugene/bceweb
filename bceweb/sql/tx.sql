SELECT DISTINCT
  id,
  b_id,
  hash,
  (SELECT COUNT(*) FROM vout WHERE t_id_in = {tx}),
  (SELECT COUNT(*) FROM vout WHERE t_id = {tx})
FROM tx
WHERE id = {tx};