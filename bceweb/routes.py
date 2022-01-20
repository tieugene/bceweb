"""
:todo: link user/session with cursor
"""
import math
from flask import Blueprint, render_template, request

import vars

PAGE_SIZE = 25
Q_DATES_COUNT = 'SELECT COUNT(DISTINCT DATE(datime)) FROM bk;'
Q_DATES = 'SELECT DISTINCT DATE(datime) AS date, COUNT(*) AS num FROM bk GROUP BY date ORDER BY date OFFSET {offset} LIMIT {limit};'

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
    """List dates
    """
    pages = math.ceil(get_count(Q_DATES_COUNT) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = vars.CONN.cursor()
    cur.execute(Q_DATES.format(limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_dates.html', data=cur, pager=(page, pages))


'''
@bp.route('/src/date/<int:d>', methods=['GET'])
def src_bks():
    """List blocks of date"""
    ...


@bp.route('/src/bk/<int:bk>', methods=['GET'])
def src_bks():
    """List txs of block"""
    ...


@bp.route('/src/tx/<int:tx>', methods=['GET'])
def src_bks():
    """List vins and vouts of tx"""
    ...
'''
