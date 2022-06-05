-- Select values by dates for qid and rid
SELECT d, val FROM t_1a_date WHERE (qid={qid}) AND (rid={rid}) AND (d BETWEEN '{date0}' AND '{date1}') ORDER BY d;
