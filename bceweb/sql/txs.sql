SELECT
   id,
   b_id,
   hash,
   (SELECT COUNT(*) FROM vout WHERE vout.t_id_in = tx.id),
   (SELECT COUNT(*) FROM vout WHERE vout.t_id = tx.id),
   (SELECT SUM(money) FROM vout WHERE vout.t_id = tx.id)
FROM tx
WHERE b_id = {bk}
ORDER BY id ASC
OFFSET {offset} LIMIT {limit};