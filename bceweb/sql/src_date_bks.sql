SELECT
   id,
   datime,
   (SELECT COUNT(*) FROM tx WHERE tx.b_id = bk.id GROUP BY bk.id) AS tx_num
FROM bk
WHERE DATE(datime) = '{date}'
ORDER BY id
OFFSET {offset} LIMIT {limit};