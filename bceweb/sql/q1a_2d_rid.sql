-- Select values by rid for qid and date
SELECT rid, val FROM t_1a_date WHERE qid = {qid} AND d = '{date0}' ORDER BY rid;
