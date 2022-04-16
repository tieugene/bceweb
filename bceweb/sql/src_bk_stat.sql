SELECT * FROM (
SELECT DISTINCT
  bk.*,
  t_stat_bk.*,
  SUM(price) OVER w AS price_inc,
  SUM(tx_num) OVER w AS tx_num_inc,
  SUM(so_num) OVER w AS so_num_inc,
  SUM(so_sum) OVER w AS so_sum_inc,
  SUM(lo_num) OVER w AS lo_num_inc,
  SUM(lo_sum) OVER w AS lo_sum_inc,
  SUM(uo_num) OVER w AS uo_num_inc,
  SUM(uo_sum) OVER w AS uo_sum_inc
FROM bk
LEFT JOIN t_stat_bk ON bk.id = t_stat_bk.b_id
WINDOW w AS (ORDER BY b_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
) AS q WHERE id = {bk};
