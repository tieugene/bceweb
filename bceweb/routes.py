"""Main router"""

import math
from flask import Blueprint, render_template, request
import psycopg2


import vars
from queries import Qry

PAGE_SIZE = 25

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


def __get_records(q: str, data: dict = None):
    cur = vars.CONN.cursor()
    cur.execute(q, data)
    return cur


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/src/dates', methods=['GET'])
def src_dates():
    """List dates"""
    pages = math.ceil(__get_a_value(Qry.get('DATES_COUNT')) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Qry.get('DATES').format(limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_dates.html', data=cur, pager=(page, pages))


@bp.route('/src/bks/<d>', methods=['GET'])
def src_bks(d: str):
    """List blocks of date"""
    # date = datetime.date.fromisoformat(d)
    pages = math.ceil(__get_a_value(Qry.get('BLOCKS_COUNT').format(date=d)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Qry.get('BLOCKS').format(date=d, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_blocks.html', date=d, data=cur, pager=(page, pages))


@bp.route('/src/txs/<int:bk>', methods=['GET'])
def src_txs(bk: int):
    """List txs of block"""
    pages = math.ceil(__get_a_value(Qry.get('TXS_COUNT').format(bk=bk)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    block = __get_a_record(Qry.get('BLOCK').format(bk=bk))
    cur = __get_records(Qry.get('TXS').format(bk=bk, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_txs.html', block=block, data=cur, pager=(page, pages))


@bp.route('/src/vins/<int:tx>', methods=['GET'])
def src_vins(tx: int):
    """List vins of tx"""
    if (pages := math.ceil(__get_a_value(Qry.get('VINS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Qry.get('TX').format(tx=tx))
    block = __get_a_record(Qry.get('BLOCK').format(bk=tx_rec[1]))
    cur = __get_records(Qry.get('VINS').format(tx=tx, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_vins.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/src/vouts/<int:tx>', methods=['GET'])
def src_vouts(tx: int):
    """List vouts of tx"""
    if (pages := math.ceil(__get_a_value(Qry.get('VOUTS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Qry.get('TX').format(tx=tx))
    block = __get_a_record(Qry.get('BLOCK').format(bk=tx_rec[1]))
    cur = __get_records(Qry.get('VOUTS').format(tx=tx, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_vouts.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/src/addr/<int:aid>', methods=['GET'])
def src_addr(aid: int):
    """List of address operations"""
    pages = math.ceil(__get_a_value(Qry.get('ADDR_MOVES_COUNT').format(aid=aid)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    addr = __get_a_record(Qry.get('ADDR').format(aid=aid))
    cur = __get_records(Qry.get('ADDR_MOVES').format(aid=aid, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_addr.html', addr=addr, data=cur, pager=(page, pages))
