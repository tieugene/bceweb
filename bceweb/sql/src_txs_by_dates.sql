SELECT
  MIN(tx.id) AS tx_id_min,
  MAX(tx.id) AS tx_id_max
FROM
  tx
LEFT JOIN bk ON tx.b_id = bk.id
WHERE DATE(bk.datime) >= '{date0}' AND DATE(bk.datime) <= '{date1}';
