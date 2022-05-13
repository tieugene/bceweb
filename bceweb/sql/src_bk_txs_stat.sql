SELECT DISTINCT
  COUNT(*) AS tx_num,
  MIN(id) AS tx_min,
  MAX(id) AS tx_max
FROM tx
WHERE b_id = {bk};
