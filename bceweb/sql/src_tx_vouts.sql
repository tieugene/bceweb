SELECT
   t_id,
   n,
   t_id_in,
   money,
   a_id,
   addr.name AS a_name,
   addr.qty AS a_num
FROM vout
    LEFT JOIN addr ON addr.id = vout.a_id
WHERE t_id = {tx}
ORDER BY t_id ASC, n ASC
OFFSET {offset} LIMIT {limit};