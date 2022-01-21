"""SQL queries storage"""


class Qry(dict):
    __storage: dict = {
        'DATES_COUNT': "SELECT COUNT(DISTINCT DATE(datime)) FROM bk;",
        'DATES': "SELECT DISTINCT DATE(datime) AS date, COUNT(*) AS num FROM bk GROUP BY date ORDER BY date ASC OFFSET {offset} LIMIT {limit};",
        'BLOCKS_COUNT': "SELECT COUNT(*) FROM bk WHERE DATE(datime) = '{date}';",
        'BLOCKS': "SELECT id, datime, (SELECT COUNT(*) FROM tx WHERE tx.b_id = bk.id GROUP BY bk.id) FROM bk WHERE DATE(datime) = '{date}' ORDER BY id ASC OFFSET {offset} LIMIT {limit};",
        'BLOCK': "SELECT DISTINCT id, datime FROM bk WHERE id = {bk};",
        'TXS_COUNT': "SELECT COUNT(*) FROM tx WHERE b_id = {bk};",
        'TXS': "SELECT id, b_id, hash, (SELECT COUNT(*) FROM vout WHERE vout.t_id_in = tx.id), (SELECT COUNT(*) FROM vout WHERE vout.t_id = tx.id), (SELECT SUM(money) FROM vout WHERE vout.t_id = tx.id) FROM tx WHERE b_id = {bk} ORDER BY id ASC OFFSET {offset} LIMIT {limit};",
        'TX': "SELECT DISTINCT id, b_id, hash, (SELECT COUNT(*) FROM vout WHERE t_id_in = {tx}), (SELECT COUNT(*) FROM vout WHERE t_id = {tx}) FROM tx WHERE id = {tx};",
        'VINS_COUNT': "SELECT COUNT(*) FROM vout WHERE t_id_in = {tx};",
        'VINS': "SELECT t_id, n, t_id_in, money, a_id, addr.name, addr.qty FROM vout LEFT JOIN addr ON addr.id = vout.a_id WHERE t_id_in = {tx} ORDER BY t_id ASC, n ASC OFFSET {offset} LIMIT {limit};",
        'VOUTS_COUNT': "SELECT COUNT(*) FROM vout WHERE t_id = {tx};",
        'VOUTS': "SELECT t_id, n, t_id_in, money, a_id, addr.name, addr.qty FROM vout LEFT JOIN addr ON addr.id = vout.a_id WHERE t_id = {tx} ORDER BY t_id ASC, n ASC OFFSET {offset} LIMIT {limit};",
        'ADDR': "SELECT DISTINCT id, name, qty, (SELECT SUM(money) FROM vout WHERE a_id = {aid} AND t_id_in IS NULL) FROM addr WHERE id = {aid};",
        'ADDR_MOVES_COUNT': "SELECT COUNT(*) FROM vout WHERE a_id = {aid};",
        'ADDR_MOVES': "SELECT t_id, n, t_id_in, money FROM vout WHERE a_id = {aid} ORDER BY t_id ASC, n ASC OFFSET {offset} LIMIT {limit};",
    }

    @staticmethod
    def get(name: str):
        return Qry.__storage.get(name)
