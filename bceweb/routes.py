"""
:todo: X-links
:todo: format money (BTC, dec separator)
:todo: ext links as pic
"""
import math
from flask import Blueprint, render_template, request

import vars

PAGE_SIZE = 25
Q_DATES_COUNT = "SELECT COUNT(DISTINCT DATE(datime)) FROM bk;"
Q_DATES = "SELECT DISTINCT DATE(datime) AS date, COUNT(*) AS num FROM bk GROUP BY date ORDER BY date ASC OFFSET {offset} LIMIT {limit};"
Q_BLOCKS_COUNT = "SELECT COUNT(*) FROM bk WHERE DATE(datime) = '{date}';"
Q_BLOCKS = "SELECT id, datime, (SELECT COUNT(*) FROM tx WHERE tx.b_id = bk.id GROUP BY bk.id) FROM bk WHERE DATE(datime) = '{date}' ORDER BY id ASC OFFSET {offset} LIMIT {limit};"
Q_BLOCK = "SELECT DISTINCT id, datime FROM bk WHERE id = {bk};"
Q_TXS_COUNT = "SELECT COUNT(*) FROM tx WHERE b_id = {bk};"
Q_TXS = "SELECT id, b_id, hash, (SELECT COUNT(*) FROM vout WHERE vout.t_id_in = tx.id), (SELECT COUNT(*) FROM vout WHERE vout.t_id = tx.id), (SELECT SUM(money) FROM vout WHERE vout.t_id = tx.id) FROM tx WHERE b_id = {bk} ORDER BY id ASC OFFSET {offset} LIMIT {limit};"
Q_TX = "SELECT DISTINCT id, b_id, hash FROM tx WHERE id = {tx};"
Q_VINS_COUNT = "SELECT COUNT(*) FROM vout WHERE t_id_in = {tx};"
Q_VINS = "SELECT t_id, n, t_id_in, money, a_id, addr.name, addr.qty FROM vout LEFT JOIN addr ON addr.id = vout.a_id WHERE t_id_in = {tx} ORDER BY t_id ASC, n ASC OFFSET {offset} LIMIT {limit};"
Q_VOUTS_COUNT = "SELECT COUNT(*) FROM vout WHERE t_id = {tx};"
Q_VOUTS = "SELECT t_id, n, t_id_in, money, a_id, addr.name, addr.qty FROM vout LEFT JOIN addr ON addr.id = vout.a_id WHERE t_id = {tx} ORDER BY t_id ASC, n ASC OFFSET {offset} LIMIT {limit};"
Q_ADDR = "SELECT DISTINCT id, name, qty, (SELECT SUM(money) FROM vout WHERE a_id = {aid} AND t_id_in IS NULL) FROM addr WHERE id = {aid};"
Q_ADDR_MOVES_COUNT = "SELECT COUNT(*) FROM vout WHERE a_id = {aid};"
Q_ADDR_MOVES = "SELECT t_id, n, t_id_in, money FROM vout WHERE a_id = {aid} ORDER BY t_id ASC, n ASC OFFSET {offset} LIMIT {limit};"

bp = Blueprint('bceweb', __name__)


def __get_a_value(q: str) -> int:
    """Get single value from query.
    :param q: query text to execute
    :return: value get
    """
    return __get_a_record(q)[0]


def __get_a_record(q: str) -> list:
    """Get single record from query.
    :param q: query text to execute
    :return: value get
    """
    return __get_records(q).fetchone()


def __get_records(q: str):
    cur = vars.CONN.cursor()
    cur.execute(q)
    return cur


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/src/dates', methods=['GET'])
def src_dates():
    """List dates"""
    pages = math.ceil(__get_a_value(Q_DATES_COUNT) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Q_DATES.format(limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_dates.html', data=cur, pager=(page, pages))


@bp.route('/src/bks/<d>', methods=['GET'])
def src_bks(d: str):
    """List blocks of date"""
    # date = datetime.date.fromisoformat(d)
    pages = math.ceil(__get_a_value(Q_BLOCKS_COUNT.format(date=d)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Q_BLOCKS.format(date=d, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_blocks.html', date=d, data=cur, pager=(page, pages))


@bp.route('/src/txs/<int:bk>', methods=['GET'])
def src_txs(bk: int):
    """List txs of block"""
    pages = math.ceil(__get_a_value(Q_TXS_COUNT.format(bk=bk)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    block = __get_a_record(Q_BLOCK.format(bk=bk))
    cur = __get_records(Q_TXS.format(bk=bk, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_txs.html', block=block, data=cur, pager=(page, pages))


@bp.route('/src/vins/<int:tx>', methods=['GET'])
def src_vins(tx: int):
    """List vins of tx"""
    pages = math.ceil(__get_a_value(Q_VINS_COUNT.format(tx=tx)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Q_TX.format(tx=tx))
    block = __get_a_record(Q_BLOCK.format(bk=tx_rec[1]))
    cur = __get_records(Q_VINS.format(tx=tx, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_vins.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/src/vouts/<int:tx>', methods=['GET'])
def src_vouts(tx: int):
    """List vouts of tx"""
    pages = math.ceil(__get_a_value(Q_VOUTS_COUNT.format(tx=tx)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Q_TX.format(tx=tx))
    block = __get_a_record(Q_BLOCK.format(bk=tx_rec[1]))
    cur = __get_records(Q_VOUTS.format(tx=tx, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_vouts.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/src/addr/<int:aid>', methods=['GET'])
def src_addr(aid: int):
    """List of address operations"""
    pages = math.ceil(__get_a_value(Q_ADDR_MOVES_COUNT.format(aid=aid)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    addr = __get_a_record(Q_ADDR.format(aid=aid))
    cur = __get_records(Q_ADDR_MOVES.format(aid=aid, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_addr.html', addr=addr, data=cur, pager=(page, pages))
