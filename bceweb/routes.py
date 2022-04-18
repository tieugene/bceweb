"""Main router"""
# 1. std
from typing import Optional
import datetime
import io
import math
import calendar
import pprint
# 2. 3rd
import sys

import psycopg2
import psycopg2.extras
from flask import Blueprint, render_template, request, send_file, g, current_app

# 3. local
from . import forms, xlstore
from .queries import Qry

PAGE_SIZE = 25

bp = Blueprint('bceweb', __name__)


# utils
# - misc
def __timestamp() -> int:
    return int(datetime.datetime.now().timestamp())


def __now() -> datetime.datetime:
    return datetime.datetime.now().replace(microsecond=0)


# - db
def __get_db():
    if (db := g.get('_database')) is None:
        # db = g._database = psycopg2.extras.NamedTupleConnection(
        db = g._database = psycopg2.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            database=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASS']
        )
    return db


def __get_a_value(q: str) -> (int, datetime.date):
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
    cur = __get_db().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    # cur = __get_db().cursor()
    cur.execute(q, data)
    return cur


# filters
@bp.add_app_template_filter
def intorna(i: Optional[int]) -> str:
    """Convert int to str or 'n/a'."""
    return "{:,}".format(i).replace(',', ' ') if i is not None else 'n/a'


@bp.add_app_template_filter
def sa2btc(sat: Optional[int]) -> str:
    """Convert satoshi to btc."""
    return "{:,.8f}".format(sat / 100000000).replace(',', ' ') if sat is not None else 'n/a'


# routes
@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/y/', methods=['GET'])
def src_years():
    # TODO: redirect
    max_year = int(__get_a_value(Qry.get('SRC_MAX_YEAR')))  # FIXME: what if None
    return render_template('src_years.html', data={'max_year': max_year})


@bp.route('/y/<int:y>/', methods=['GET'])
def src_year(y: int):
    """Year calendar.
    :param y: Year (2009+)
    :note: Special: 2009 (2009-01-03, 2009-01-09+)
    :todo: chk year by DB
    :todo: fix if max_doy(2009) < '2009-01-31'
    """
    max_year = int(__get_a_value(Qry.get('SRC_MAX_YEAR')))
    iy = int(y)
    max_doy: datetime.date = __get_a_value(Qry.get('SRC_MAX_DOY').format(year=iy))
    # print(max_doy)
    months = []
    for m in range(max_doy.month - 1):
        # print(calendar.monthrange(int(y), m+1))
        months.append([d + 1 for d in range(calendar.monthrange(iy, m + 1)[1])])
    months.append([d + 1 for d in range(max_doy.day)])
    if iy == 2009:  # special case
        months[0][0:8] = [None, None, 3, None, None, None, None, None]
    # for m in data:
    #    print(m)
    return render_template('src_year.html', data={'max_year': max_year, 'year': iy, 'months': months})


@bp.route('/m/<int:y>/<int:m>/', methods=['GET'])
def src_month(y: int, m: int):
    """Month calendar.
    :param y: Year (2009+)
    :param m: Month (1..12)
    :todo: chk y in DB & m == 1..12
    """
    iy = int(y)
    im = int(m)
    max_year = int(__get_a_value(Qry.get('SRC_MAX_YEAR')))
    max_month = int(__get_a_value(Qry.get('SRC_MAX_MOY').format(year=iy)))
    dom_list = __get_records(Qry.get('SRC_DOM_LIST').format(year=iy, month=im))
    return render_template('src_month.html', data={
        'max_year': max_year,
        'year': iy,
        'max_month': max_month,
        'month': im,
        'dates': dom_list
    })


@bp.route('/d/<int:y>/<int:m>/<int:d>/', methods=['GET'])
def src_date(y: int, m: int, d: int):
    """Date's blocks.
    :param y: Year (2009+)
    :param m: Month (1..12)
    :param d: Day of month (1..31)
    :todo: chk y (in db), m (1..12 and in DB), d (1..31 and in month and in DB)
    """
    iy = int(y)
    im = int(m)
    date = datetime.date(iy, im, int(d))
    max_dom = int(__get_a_value(Qry.get('SRC_MAX_DOM').format(year=iy, month=im)))
    pages = math.ceil(__get_a_value(Qry.get('SRC_DATE_BKS_COUNT').format(date=date)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    blocks = __get_records(Qry.get('SRC_DATE_BKS').format(date=date, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_date.html', pager=(page, pages), data={
        'max_dom': max_dom,
        'date': date,
        'blocks': blocks
    })


@bp.route('/b/', methods=['GET'])
def src_bk_list():
    """Blocks available.
    :todo: rm?
    """
    pages = math.ceil(__get_a_value(Qry.get('SRC_BK_MAX')) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    data = __get_records(Qry.get('SRC_BK_LIST').format(limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_bk_list.html', pager=(page, pages), data=data)


@bp.route('/b/<int:bk>/', methods=['GET'])
def src_bk(bk: int):
    """Block info (stat).
    :todo: check bk <= bk_max & in DB
    """

    def mustb(i):
        return (((1 << ((i // 210000) + 1)) - 2) * 210000 + (i % 210000) + 1) * (5000000000 >> (i // 210000))

    ibk = int(bk)
    bk_max = __get_a_value(Qry.get('SRC_BK_MAX'))  # ??? bk_max <> bk_count
    block = __get_a_record(Qry.get('SRC_BK_STAT').format(bk=bk))
    return render_template('src_bk_stat.html', block=block, bk_max=bk_max, mustb=mustb(ibk))


@bp.route('/b/<int:bk>/t/', methods=['GET'])
def src_bk_txs(bk: int):
    """Block's TXs"""
    pages = math.ceil(__get_a_value(Qry.get('SRC_BK_TXS_COUNT').format(bk=bk)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    block = __get_a_record(Qry.get('SRC_BK').format(bk=bk))
    cur = __get_records(Qry.get('SRC_BK_TXS').format(bk=bk, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_bk_txs.html', block=block, data=cur, pager=(page, pages))


@bp.route('/t/<int:tx>/i/', methods=['GET'])
def src_tx_vins(tx: int):
    """TX's vins"""
    if (pages := math.ceil(__get_a_value(Qry.get('SRC_TX_VINS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Qry.get('SRC_TX').format(tx=tx))
    block = __get_a_record(Qry.get('SRC_BK').format(bk=tx_rec[1]))  # ! not 'b_id'
    cur = __get_records(Qry.get('SRC_TX_VINS').format(tx=tx, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_tx_vins.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/t/<int:tx>/o/', methods=['GET'])
def src_tx_vouts(tx: int):
    """TX's vouts"""
    if (pages := math.ceil(__get_a_value(Qry.get('SRC_TX_VOUTS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Qry.get('SRC_TX').format(tx=tx))
    block = __get_a_record(Qry.get('SRC_BK').format(bk=tx_rec[1]))  # ! not 'b_id'
    cur = __get_records(Qry.get('SRC_TX_VOUTS').format(tx=tx, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_tx_vouts.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/a/<int:aid>/', methods=['GET'])
def src_addr(aid: int):
    """Address' operations"""
    pages = math.ceil(__get_a_value(Qry.get('SRC_ADDR_MOVES_COUNT').format(aid=aid)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    addr = __get_a_record(Qry.get('SRC_ADDR').format(aid=aid))
    cur = __get_records(Qry.get('SRC_ADDR_MOVES').format(aid=aid, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_addr.html', addr=addr, data=cur, pager=(page, pages))


@bp.route('/i/', methods=['GET'])
def info():
    data = dict()
    data['bk'] = __get_a_record(Qry.get('INFO_BK'))
    data['txo'] = __get_a_record(Qry.get('INFO_TXO'))
    return render_template('info.html', data=data)


@bp.route('/q/', methods=['GET'])
def q_index():
    """List of queries"""
    return render_template('q_index.html')


@bp.route('/xl/<int:xl_id>/', methods=['GET'])
def get_xl(xl_id: int):
    """Get previously created XLSX"""
    if data := xlstore.Store.get(xl_id):
        return send_file(io.BytesIO(data), download_name=f"{xl_id}.xlsx")


# diffs: head:list, title:str, query
def __q_addr_x_y(formclass, title: str, head: tuple, qry_name: str, tpl_name: str, btc_cols: set = frozenset):
    form = formclass()
    data = []
    times = None
    xl_id = 0
    if form.validate_on_submit():
        num = form.num.data
        date0 = form.date0.data if 'date0' in form.data else None
        date1 = form.date1.data
        time0 = __now()
        cur = __get_records(Qry.get(qry_name).format(num=num, date0=date0, date1=date1))
        data = cur.fetchall()
        time1 = __now()
        times = (time0, time1)
        title = title.format(num=num, date0=date0, date1=date1)
        meta = {'title': title, 'subject': '', 'created': time1, 'comments': ''}
        xl_id = xlstore.mk_xlsx(meta, head, data, btc_cols)
    return render_template(tpl_name, title=title, head=head, data=data, form=form, times=times, xl_id=xl_id)


@bp.route('/q/addr_btc_max/', methods=['GET', 'POST'])
def q_addr_btc_max():
    """Top [num] addresses by gain (₿) in period [fromdate]...[todate]"""
    return __q_addr_x_y(
        forms.ND0D1Form,
        "Топ {num} адресов по увеличению баланса (₿) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Profit'),
        'Q_ADDR_BTC_MAX',
        'q_addr_btc_.html',
        {2, 3, 4}
    )


@bp.route('/q/addr_btc_min/', methods=['GET', 'POST'])
def q_addr_btc_min():
    """Top [num] addresses by lost (₿) in period [fromdate]...[todate]"""
    return __q_addr_x_y(
        forms.ND0D1Form,
        "Топ {num} адресов по уменьшению баланса (₿) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Profit'),
        'Q_ADDR_BTC_MIN',
        'q_addr_btc_.html',
        {2, 3, 4}
    )


@bp.route('/q/addr_cnt_max/', methods=['GET', 'POST'])
def q_addr_cnt_max():
    """Top [num] addresses by gain (%) in period [fromdate]...[todate]"""
    return __q_addr_x_y(
        forms.ND0D1Form,
        "Топ {num} адресов по увеличению баланса (%) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Рост, %'),
        'Q_ADDR_CNT_MAX',
        'q_addr_cnt_.html',
        {2, 3}
    )


@bp.route('/q/addr_cnt_min/', methods=['GET', 'POST'])
def q_addr_cnt_min():
    """Top [num] addresses by lost (%) in period [fromdate]...[todate]"""
    return __q_addr_x_y(
        forms.ND0D1Form,
        "Топ {num} адресов по уменьшению баланса (%) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Рост, %'),
        'Q_ADDR_CNT_MIN',
        'q_addr_cnt_.html',
        {2, 3}
    )


@bp.route('/q/addr_gt/', methods=['GET', 'POST'])
def q_addr_gt():
    """Addresses with balance > [num] sat. on [date]"""
    return __q_addr_x_y(
        forms.ND1Form,
        "Адреса с балансом > {num} sat. на {date1}",
        ("a_id", "Адрес", "Баланс, ₿"),
        'Q_ADDR_GT',
        'q_addr_gt.html',
        {2}
    )


def __q_addr_x_y_tx(formclass, title: str, head: tuple, qry_name: str, tpl_name: str, btc_cols: set = frozenset):
    form = formclass()
    data = []
    times = None
    xl_id = 0
    if form.validate_on_submit():
        num = form.num.data
        date0 = form.date0.data if 'date0' in form.data else None
        date1 = form.date1.data
        # TODO: dates to txs
        txs = __get_a_record(Qry.get('SRC_TXS_BY_DATES').format(date0=date0 or date1, date1=date1))
        time0 = __now()
        cur = __get_records(Qry.get(qry_name).format(num=num, tid0=txs[0], tid1=txs[1]))
        data = cur.fetchall()
        time1 = __now()
        times = (time0, time1)
        title = title.format(num=num, date0=date0, date1=date1)
        meta = {'title': title, 'subject': '', 'created': time1, 'comments': ''}
        xl_id = xlstore.mk_xlsx(meta, head, data, btc_cols)
    return render_template(tpl_name, title=title, head=head, data=data, form=form, times=times, xl_id=xl_id)


@bp.route('/q/addr_btc_max_tx/', methods=['GET', 'POST'])
def q_addr_btc_max_tx():
    """Top [num] addresses by gain (₿) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по увеличению баланса (₿) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Profit'),
        'Q_ADDR_BTC_MAX_TX',
        'q_addr_btc_.html',
        {2, 3, 4}
    )


@bp.route('/q/addr_btc_min_tx/', methods=['GET', 'POST'])
def q_addr_btc_min_tx():
    """Top [num] addresses by lost (₿) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по уменьшению баланса (₿) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Profit'),
        'Q_ADDR_BTC_MIN_TX',
        'q_addr_btc_.html',
        {2, 3, 4}
    )


@bp.route('/q/addr_cnt_max_tx/', methods=['GET', 'POST'])
def q_addr_cnt_max_tx():
    """Top [num] addresses by gain (%) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по увеличению баланса (%) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Рост, %'),
        'Q_ADDR_CNT_MAX_TX',
        'q_addr_cnt_.html',
        {2, 3}
    )


@bp.route('/q/addr_cnt_min_tx/', methods=['GET', 'POST'])
def q_addr_cnt_min_tx():
    """Top [num] addresses by lost (%) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по уменьшению баланса (%) за {date0}...{date1}",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Рост, %'),
        'Q_ADDR_CNT_MIN_TX',
        'q_addr_cnt_.html',
        {2, 3}
    )


@bp.route('/q/addr_gt_tx/', methods=['GET', 'POST'])
def q_addr_gt_tx():
    """Addresses with balance > [num] sat. on [date]"""
    return __q_addr_x_y_tx(
        forms.ND1Form,
        "Адреса с балансом > {num} sat. на {date1}",
        ("a_id", "Адрес", "Баланс, ₿"),
        'Q_ADDR_GT_TX',
        'q_addr_gt.html',
        {2}
    )
