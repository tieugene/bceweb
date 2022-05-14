-- Pivot table
-- Pre: CREATE EXTENSION IF NOT EXISTS tablefunc;
SELECT * FROM crosstab(
    $$ SELECT d, rid, val FROM t_1a_date WHERE (qid = {qid}) AND (d BETWEEN '{date0}' AND '{date1}') ORDER BY d, rid; $$
) AS (d DATE, rid1 BIGINT, rid2 BIGINT, rid3 BIGINT, rid4 BIGINT, rid5 BIGINT, rid6 BIGINT, rid7 BIGINT, rid8 BIGINT, rid9 BIGINT, rid10 BIGINT, rid11 BIGINT)
ORDER BY d;
