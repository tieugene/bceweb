SELECT
    a_id,
    addr.name as address,
    itogo
FROM (
    SELECT a_id, sum(money) as itogo
    FROM txo
    WHERE
        (date0 < '{date1}')
        AND (date1 >= '{date1}' OR date1 IS NULL)
    GROUP BY a_id
    HAVING SUM(money) >= {num}
) AS data INNER JOIN addr ON data.a_id = addr.id
ORDER BY itogo DESC, a_id;
