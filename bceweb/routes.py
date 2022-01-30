"""Main router"""
# 1. std
import datetime
import io
import math

# 2. 3rd
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
    cur = __get_db().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    # cur = __get_db().cursor()
    cur.execute(q, data)
    return cur


# filters
@bp.add_app_template_filter
def sa2btc(sat: int) -> str:
    """Convert satoshi to btc."""
    return "{:.8f}".format(sat/100000000)


# routes
@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/src/dates', methods=['GET'])
def src_dates():
    """Dates available"""
    pages = math.ceil(__get_a_value(Qry.get('SRC_DATES_COUNT')) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Qry.get('SRC_DATES').format(limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_dates.html', data=cur, pager=(page, pages))


@bp.route('/src/date/<d>/bks', methods=['GET'])
def src_date_bks(d: str):
    """Date's blocks"""
    # date = datetime.date.fromisoformat(d)
    pages = math.ceil(__get_a_value(Qry.get('SRC_DATE_BKS_COUNT').format(date=d)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Qry.get('SRC_DATE_BKS').format(date=d, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_date_bks.html', date=d, data=cur, pager=(page, pages))


@bp.route('/src/bk/<int:bk>', methods=['GET'])
def src_bk(bk: int):
    """Block info (stat)"""
    pages = math.ceil(__get_a_value(Qry.get('SRC_BK_TXS_COUNT').format(bk=bk)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    block = __get_a_record(Qry.get('SRC_BK').format(bk=bk))
    cur = __get_records(Qry.get('SRC_BK_TXS').format(bk=bk, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_bk_stat.html', block=block, data=cur, pager=(page, pages))


@bp.route('/src/bk/<int:bk>/txs', methods=['GET'])
def src_bk_txs(bk: int):
    """Block's TXs"""
    pages = math.ceil(__get_a_value(Qry.get('SRC_BK_TXS_COUNT').format(bk=bk)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    block = __get_a_record(Qry.get('SRC_BK').format(bk=bk))
    cur = __get_records(Qry.get('SRC_BK_TXS').format(bk=bk, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_bk_txs.html', block=block, data=cur, pager=(page, pages))


@bp.route('/src/tx/<int:tx>/vins', methods=['GET'])
def src_tx_vins(tx: int):
    """TX's vins"""
    if (pages := math.ceil(__get_a_value(Qry.get('SRC_TX_VINS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Qry.get('SRC_TX').format(tx=tx))
    block = __get_a_record(Qry.get('SRC_BK').format(bk=tx_rec[1]))  # ! not 'b_id'
    cur = __get_records(Qry.get('SRC_TX_VINS').format(tx=tx, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_tx_vins.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/src/tx/<int:tx>/vouts', methods=['GET'])
def src_tx_vouts(tx: int):
    """TX's vouts"""
    if (pages := math.ceil(__get_a_value(Qry.get('SRC_TX_VOUTS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    tx_rec = __get_a_record(Qry.get('SRC_TX').format(tx=tx))
    block = __get_a_record(Qry.get('SRC_BK').format(bk=tx_rec[1]))  # ! not 'b_id'
    cur = __get_records(Qry.get('SRC_TX_VOUTS').format(tx=tx, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_tx_vouts.html', block=block, tx=tx_rec, data=cur, pager=(page, pages))


@bp.route('/src/addr/<int:aid>', methods=['GET'])
def src_addr(aid: int):
    """Address' operations"""
    pages = math.ceil(__get_a_value(Qry.get('SRC_ADDR_MOVES_COUNT').format(aid=aid)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    addr = __get_a_record(Qry.get('SRC_ADDR').format(aid=aid))
    cur = __get_records(Qry.get('SRC_ADDR_MOVES').format(aid=aid, limit=PAGE_SIZE, offset=(page-1) * PAGE_SIZE))
    return render_template('src_addr.html', addr=addr, data=cur, pager=(page, pages))


@bp.route('/info', methods=['GET'])
def info():
    data = dict()
    data['bk'] = __get_a_record(Qry.get('INFO_BK'))
    data['txo'] = __get_a_record(Qry.get('INFO_TXO'))
    return render_template('info.html', data=data)


@bp.route('/q', methods=['GET'])
def q_index():
    """List of queries"""
    return render_template('q_index.html')


@bp.route('/xl/<int:xl_id>', methods=['GET'])
def get_xl(xl_id: int):
    """Get previously created XLSX"""
    if data := xlstore.Store.get(xl_id):
        return send_file(io.BytesIO(data), download_name=f"{xl_id}.xlsx")


# diffs: head:list, title:str, query
def __q_addr_x_y(formclass, title: str, head: tuple, qry_name: str, tpl_name: str, btc_cols: set = {}):
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


@bp.route('/q/addr_btc_max', methods=['GET', 'POST'])
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


@bp.route('/q/addr_btc_min', methods=['GET', 'POST'])
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


@bp.route('/q/addr_cnt_max', methods=['GET', 'POST'])
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


@bp.route('/q/addr_cnt_min', methods=['GET', 'POST'])
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


@bp.route('/q/addr_gt', methods=['GET', 'POST'])
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
