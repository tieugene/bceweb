SELECT
   id,
   b_id,
   hash,
   (SELECT COUNT(*) FROM vout WHERE vout.t_id_in = tx.id) AS vi_num,
   (SELECT COUNT(*) FROM vout WHERE vout.t_id = tx.id) AS vo_num,
   (SELECT SUM(money) FROM vout WHERE vout.t_id = tx.id) AS money
FROM tx
WHERE b_id = {bk}
ORDER BY id ASC
OFFSET {offset} LIMIT {limit};