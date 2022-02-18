SELECT
    a_id,
    addr.name AS a_name,
    itogo0,
    itogo1,
    profit
FROM (
    SELECT
        e.a_id AS a_id,
        b.itogo AS itogo0,
        e.itogo AS itogo1,
        e.itogo-COALESCE(b.itogo, 0) AS profit
    FROM (
        SELECT a_id, SUM(money) AS itogo
        FROM vout
        WHERE
            (t_id < '{tid0}')
            AND (t_id_in >= '{tid0}' OR t_id_in IS NULL)
        GROUP BY a_id
    ) AS b RIGHT JOIN (
        SELECT a_id, SUM(money) AS itogo
        FROM vout
        WHERE
            (t_id <= '{tid1}')
            AND (t_id_in > '{tid1}' OR t_id_in IS NULL)
        GROUP BY a_id
    ) AS e ON b.a_id = e.a_id
    ORDER BY profit DESC , a_id
    LIMIT {num}
) AS data INNER JOIN addr ON a_id = addr.id;
