SELECT DISTINCT
    id,
    name,
    qty,
    (SELECT SUM(money) FROM vout WHERE a_id = {aid} AND t_id_in IS NULL) AS money
FROM addr
WHERE id = {aid};