"""
:todo: link user/session with cursor
"""
import datetime
import math
from flask import Blueprint, render_template, request

import vars

PAGE_SIZE = 25
Q_DATES_COUNT = "SELECT COUNT(DISTINCT DATE(datime)) FROM bk;"
Q_DATES = "SELECT DISTINCT DATE(datime) AS date, COUNT(*) AS num FROM bk GROUP BY date ORDER BY date OFFSET {offset} LIMIT {limit};"
Q_BLOCKS_COUNT = "SELECT COUNT(*) FROM bk WHERE DATE(datime) = '{date}';"
Q_BLOCKS = "SELECT id, datime, (SELECT COUNT(*) FROM tx WHERE tx.b_id = bk.id GROUP BY bk.id) FROM bk WHERE DATE(datime) = '{date}' ORDER BY id OFFSET {offset} LIMIT {limit};"
Q_TXS_COUNT = "SELECT COUNT(*) FROM tx WHERE b_id = {bk};"
Q_TXS = "SELECT id, b_id, hash, (SELECT COUNT(*) FROM vout WHERE vout.t_id_in = tx.id), (SELECT COUNT(*) FROM vout WHERE vout.t_id = tx.id), (SELECT SUM(money) FROM vout WHERE vout.t_id = tx.id) FROM tx WHERE b_id = {bk} ORDER BY id OFFSET {offset} LIMIT {limit};"

bp = Blueprint('bceweb', __name__)


def get_count(q: str) -> int:
    """Get single value from query.
    :param q: query text to execute
    :return: value get
    """
    cur = vars.CONN.cursor()
    cur.execute(q)
    return cur.fetchone()[0]


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/src/dates', methods=['GET'])
def src_dates():
    """List dates"""
    pages = math.ceil(get_count(Q_DATES_COUNT) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = vars.CONN.cursor()
    cur.execute(Q_DATES.format(limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_dates.html', data=cur, pager=(page, pages))


@bp.route('/src/date/<d>', methods=['GET'])
def src_bks(d: str):
    """List blocks of date"""
    date = datetime.date.fromisoformat(d)
    pages = math.ceil(get_count(Q_BLOCKS_COUNT.format(date=d)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = vars.CONN.cursor()
    cur.execute(Q_BLOCKS.format(date=d, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_blocks.html', data=cur, pager=(page, pages))


@bp.route('/src/bk/<int:bk>', methods=['GET'])
def src_txs(bk: int):
    """List txs of block"""
    pages = math.ceil(get_count(Q_TXS_COUNT.format(bk=bk)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = vars.CONN.cursor()
    cur.execute(Q_TXS.format(bk=bk, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_txs.html', data=cur, pager=(page, pages))


@bp.route('/src/tx/<int:tx>', methods=['GET'])
def src_vins(tx: int):
    """List vins and vouts of tx"""
    ...
