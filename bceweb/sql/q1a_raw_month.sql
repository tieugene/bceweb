SELECT d, qid, rid, val FROM t_1a_date WHERE DATE_PART('year', d) = {y} AND DATE_PART('month', d) = {m} ORDER BY d, qid, rid;
