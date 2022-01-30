SELECT
    a_id,
    addr.name AS a_name,
    itogo0,
    itogo1,
    profit
FROM (
    SELECT
        b.a_id AS a_id,
        b.itogo AS itogo0,
        e.itogo AS itogo1,
        ROUND((1-b.itogo/e.itogo)*100, 0) AS profit
    FROM (
        SELECT a_id, SUM(money) AS itogo
        FROM txo
        WHERE
            (date0 < '{date0}')
            AND (date1 >= '{date0}' OR date1 IS NULL)
        GROUP BY a_id
    ) AS b INNER JOIN (
        SELECT a_id, SUM(money) AS itogo
        FROM txo
        WHERE
            (date0 <= '{date1}')
            AND (date1 > '{date1}' OR date1 IS NULL)
        GROUP BY a_id
        HAVING SUM(money) > 0
    ) AS e ON b.a_id = e.a_id
    ORDER BY profit, a_id
    LIMIT {num}
) AS data INNER JOIN addr ON a_id = addr.id;
