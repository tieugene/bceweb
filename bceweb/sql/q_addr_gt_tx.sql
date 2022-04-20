SELECT
    a_id,
    addr.name as a_name,
    itogo
FROM (
    SELECT a_id, sum(money) as itogo
    FROM {table}
    WHERE
        (t_id < '{tid1}')
        AND (t_id_in >= '{tid1}' OR t_id_in IS NULL)
    GROUP BY a_id
    HAVING SUM(money)/100000000 >= {num}
) AS data INNER JOIN addr ON data.a_id = addr.id
ORDER BY itogo DESC, a_id;
