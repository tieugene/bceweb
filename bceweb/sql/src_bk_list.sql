SELECT DISTINCT
  bk.*,
  t_bk_stat.*,
  SUM(price) OVER w AS price_inc,
  SUM(tx_num) OVER w AS tx_num_inc,
  SUM(vi_num) OVER w AS vi_num_inc,
  SUM(vo_num) OVER w AS vo_num_inc,
  SUM(so_num) OVER w AS so_num_inc,
  SUM(lo_num) OVER w AS lo_num_inc,
  SUM(uo_num) OVER w AS uo_num_inc,
  SUM(vi_sum) OVER w AS vi_sum_inc,
  SUM(vi_num_job) OVER w AS vi_num_job_inc,
  SUM(vi_sum_job) OVER w AS vi_sum_job_inc
FROM bk
LEFT JOIN t_bk_stat ON bk.id = t_bk_stat.b_id
WINDOW w AS (ORDER BY bk.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
ORDER BY bk.id
OFFSET {offset} LIMIT {limit};
