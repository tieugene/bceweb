-- Max tx.id of block
SELECT MAX(id) FROM tx WHERE b_id = {bk};
-- count (slow):
