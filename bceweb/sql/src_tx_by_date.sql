SELECT
  MIN(tx.id) AS tid0,
  MAX(tx.id) AS tid1
FROM
  tx
LEFT JOIN bk ON tx.b_id = bk.id
WHERE DATE(bk.datime) >= '{date0}' AND DATE(bk.datime) <= '{date1}';
