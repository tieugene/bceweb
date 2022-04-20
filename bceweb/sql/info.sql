SELECT
    (SELECT MAX(id) FROM bk) AS bk_id_max,
    (SELECT MAX(datime) FROM bk) AS bk_datime_max,
    (SELECT MAX(b_id) FROM t_stat_bk) AS stat_bk_max,
    (SELECT MAX(d) FROM t_stat_date) AS stat_date_max,
    (SELECT DATE(bk.datime) FROM (SELECT MIN(t_id_in) AS t_id FROM tail) AS v INNER JOIN tx ON v.t_id = tx.id INNER JOIN bk ON bk.id = tx.b_id) AS tail_date_min,
    (SELECT DATE(bk.datime) FROM (SELECT MAX(t_id) AS t_id FROM tail) AS v INNER JOIN tx ON v.t_id = tx.id INNER JOIN bk ON bk.id = tx.b_id) AS tail_date_max
;