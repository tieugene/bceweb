"""Main router"""
# 1. std
import csv
from typing import Optional, Tuple, Type, Iterable, Union
import datetime
import io
import math
import calendar
# 2. 3rd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import psycopg2
import psycopg2.extras
from flask import Blueprint, render_template, request, send_file, g, current_app, session, redirect, url_for

# 3. local
from . import forms, xlstore
from .queries import Qry

# consts
PAGE_SIZE = 25
COOKEY_YEAR = 'year'
COOKEY_FORM_NUM = 'form_num'
COOKEY_FORM_DATE0 = 'form_date0'
COOKEY_FORM_DATE1 = 'form_date1'
COOKEY_FORM_QID = 'form_qid'
COOKEY_FORM_RID = 'form_rid'
RID = (
    (1, 10**5),
    (10**5 + 1, 10**6),
    (10**6 + 1, 10**7),
    (10**7 + 1, 10**8),
    (10**8 + 1, 10**9),
    (10**9 + 1, 10**10),
    (10**10 + 1, 10**11),
    (10**11 + 1, 10**12),
    (10**12 + 1, 10**13),
    (10**13 + 1, 10**14),
    (10**14 + 1, 22 * 10**14)  # 21 M₿ is hardcoded limit
)
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


def __get_cookie(name: str, t: Optional[type] = None) -> Optional[Union[int, str, datetime.date]]:
    if name in session and (val := session.get(name)) is not None:
        return datetime.date.fromisoformat(val) if t == datetime.date else val


def __set_cookie(name: str, val: Union[int, str, datetime.date]):
    session[name] = val.isoformat() if isinstance(val, datetime.date) else val


def __update_cookie(name: str, val: Union[int, str, datetime.date]):
    if (__get_cookie(name, datetime.date) if isinstance(val, datetime.date) else __get_cookie(name)) != val:
        __set_cookie(name, val)


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
    if (y := __get_cookie(COOKEY_YEAR)) is None or y > max_year:
        y = 2009
    return redirect(url_for('bceweb.src_year', y=y))


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
    __update_cookie(COOKEY_YEAR, iy)
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
    stat = __get_a_record(Qry.get('SRC_DATE_STAT').format(date=date.isoformat()))
    max_dom = int(__get_a_value(Qry.get('SRC_MAX_DOM').format(year=iy, month=im)))
    return render_template('src_date.html', data={'max_dom': max_dom, 'date': date, 'stat': stat})


@bp.route('/d/<int:y>/<int:m>/<int:d>/b/', methods=['GET'])
def src_date_blocks(y: int, m: int, d: int):
    iy = int(y)
    im = int(m)
    date = datetime.date(iy, im, int(d))
    max_dom = int(__get_a_value(Qry.get('SRC_MAX_DOM').format(year=iy, month=im)))
    pages = math.ceil(__get_a_value(Qry.get('SRC_DATE_BKS_COUNT').format(date=date)) / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    blocks = __get_records(Qry.get('SRC_DATE_BKS').format(date=date, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_date_blocks.html', pager=(page, pages), data={'blocks': blocks})


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
    return render_template('src_bk.html', block=block, bk_max=bk_max, mustb=mustb(ibk))


@bp.route('/b/<int:bk>/t/', methods=['GET'])
def src_bk_txs(bk: int):
    """Block's TXs"""
    tx_stat = __get_a_record(Qry.get('SRC_BK_TXS_STAT').format(bk=bk))
    pages = math.ceil(tx_stat.tx_num / PAGE_SIZE)
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    block = __get_a_record(Qry.get('SRC_BK').format(bk=bk))
    cur = __get_records(Qry.get('SRC_BK_TXS').format(bk=bk, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_bk_txs.html', block=block, data=cur, pager=(page, pages))


@bp.route('/t/<int:tx>/', methods=['GET'])
def src_tx(tx: int):
    itx = int(tx)
    tx_data = __get_a_record(Qry.get('SRC_TX').format(tx=itx))
    tx_stat = __get_a_record(Qry.get('SRC_BK_TXS_STAT').format(bk=tx_data.b_id))
    print(tx_stat)
    return render_template('src_tx.html', data={'tx': tx_data, 'bk': tx_stat})


@bp.route('/t/<int:tx>/in/', methods=['GET'])
def src_tx_in(tx: int):
    if (pages := math.ceil(__get_a_value(Qry.get('SRC_TX_VINS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Qry.get('SRC_TX_VINS').format(tx=tx, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_tx_in.html', data=cur, pager=(page, pages))


@bp.route('/t/<int:tx>/out/', methods=['GET'])
def src_tx_out(tx: int):
    if (pages := math.ceil(__get_a_value(Qry.get('SRC_TX_VOUTS_COUNT').format(tx=tx)) / PAGE_SIZE)) == 0:
        pages = 1
    if (page := request.args.get('page', 1, type=int)) > pages:
        page = pages
    cur = __get_records(Qry.get('SRC_TX_VOUTS').format(tx=tx, limit=PAGE_SIZE, offset=(page - 1) * PAGE_SIZE))
    return render_template('src_tx_out.html', data=cur, pager=(page, pages))


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
    data = __get_a_record(Qry.get('INFO'))
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


def __q_addr_x_y_tx(formclass: Type, title: str, head: Tuple, qry_name: str, tpl_name: str,
                    col_fmt: dict[int: xlstore.ECellType] = {}, use_tail: bool = False):
    """Old queries.
    :param formclass: Form to handle parms
    :param title: Title of auery
    :param head: Header column titles
    :param qry_name: 'sql/q_*' filename
    :param tpl_name: HTML template filename
    :param col_fmt: columns to represent as BTC (devide by 10^-8)
    :param use_tail: Do use 'tail' table to query (default 'vout')
    """
    form = formclass()
    data = []
    times = None
    xl_id = 0
    if form.validate_on_submit():
        num = form.num.data
        __update_cookie(COOKEY_FORM_NUM, num)
        if 'date0' in form.data:
            date0 = form.date0.data
            __update_cookie(COOKEY_FORM_DATE0, date0)
        else:
            date0 = None
        date1 = form.date1.data
        __update_cookie(COOKEY_FORM_DATE1, date1)
        # TODO: dates to txs
        txs = __get_a_record(Qry.get('SRC_TXS_BY_DATES').format(date0=date0 or date1, date1=date1))
        time0 = __now()
        table = ('vout', 'tail')[int(use_tail)]
        cur = __get_records(Qry.get(qry_name).format(table=table, num=num, tid0=txs[0], tid1=txs[1]))
        data = cur.fetchall()
        time1 = __now()
        times = (time0, time1)
        title = title.format(num=num, date0=date0, date1=date1, table=table)
        meta = {'title': title, 'subject': '', 'created': time1, 'comments': ''}
        xl_id = xlstore.mk_xlsx(meta, head, data, col_fmt)
    elif request.method == 'GET':
        if num := __get_cookie(COOKEY_FORM_NUM):
            form.num.data = num
        if 'date0' in form.data:
            if date0 := __get_cookie(COOKEY_FORM_DATE0, datetime.date):
                form.date0.data = date0
        if date1 := __get_cookie(COOKEY_FORM_DATE1, datetime.date):
            form.date1.data = date1
    return render_template(tpl_name, title=title, head=head, data=data, form=form, times=times, xl_id=xl_id)


@bp.route('/q/addr_btc_max_tx/', methods=['GET', 'POST'])
def q_addr_btc_max_tx():
    """Top [num] addresses by gain (₿) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по увеличению баланса (₿) за {date0}...{date1} (using {table})",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Profit'),
        'Q_ADDR_BTC_MAX',
        'q_addr_btc_.html',
        {2: xlstore.ECellType.BTC, 3: xlstore.ECellType.BTC, 4: xlstore.ECellType.BTC},
        request.args.get('tail') is not None
    )


@bp.route('/q/addr_btc_min_tx/', methods=['GET', 'POST'])
def q_addr_btc_min_tx():
    """Top [num] addresses by lost (₿) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по уменьшению баланса (₿) за {date0}...{date1} (using {table})",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Profit'),
        'Q_ADDR_BTC_MIN',
        'q_addr_btc_.html',
        {2: xlstore.ECellType.BTC, 3: xlstore.ECellType.BTC, 4: xlstore.ECellType.BTC},
        request.args.get('tail') is not None
    )


@bp.route('/q/addr_cnt_max_tx/', methods=['GET', 'POST'])
def q_addr_cnt_max_tx():
    """Top [num] addresses by gain (%) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по увеличению баланса (%) за {date0}...{date1} (using {table})",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Рост, %'),
        'Q_ADDR_CNT_MAX',
        'q_addr_cnt_.html',
        {2: xlstore.ECellType.BTC, 3: xlstore.ECellType.BTC},
        request.args.get('tail') is not None
    )


@bp.route('/q/addr_cnt_min_tx/', methods=['GET', 'POST'])
def q_addr_cnt_min_tx():
    """Top [num] addresses by lost (%) in period [fromdate]...[todate]"""
    return __q_addr_x_y_tx(
        forms.ND0D1Form,
        "Топ {num} адресов по уменьшению баланса (%) за {date0}...{date1} (using {table})",
        ('a_id', 'Адрес', 'Было', 'Стало', 'Рост, %'),
        'Q_ADDR_CNT_MIN',
        'q_addr_cnt_.html',
        {2: xlstore.ECellType.BTC, 3: xlstore.ECellType.BTC},
        request.args.get('tail') is not None
    )


@bp.route('/q/addr_gt_tx/', methods=['GET', 'POST'])
def q_addr_gt_tx():
    """Addresses with balance > [num] sat. on [date]"""
    return __q_addr_x_y_tx(
        forms.ND1Form,
        "Адреса с балансом > {num} BTC на {date1} (using {table})",
        ("a_id", "Адрес", "Баланс, ₿"),
        'Q_ADDR_GT',
        'q_addr_gt.html',
        {2: xlstore.ECellType.BTC},
        request.args.get('tail') is not None
    )


def __q1a_raw(src: Iterable, suffix: str, xls: bool = False):
    """
    Download Q1A for period as CSV/XLSX file
    :param src: Query data
    :param suffix:
    :param xls:
    :return:
    """
    if xls:
        if data := xlstore.q1a(src):
            return send_file(
                io.BytesIO(data),
                download_name=f"q1a_{suffix}.xlsx"
            )
    else:
        with io.StringIO() as ofile:
            writer = csv.writer(ofile, dialect=csv.excel_tab())
            writer.writerow(("date", "qid", "rid", "value"))
            writer.writerows(src)
            ofile.seek(0)
            fname = f"q1a_{suffix}.csv"
            return send_file(
                io.BytesIO(ofile.read().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=fname,
                attachment_filename=fname
            )


@bp.route('/q1a/<int:y>/<int:m>/<int:d>/', methods=['GET'])
def q1a_raw_date(y: int, m: int, d: int):
    date = datetime.date(int(y), int(m), int(d))
    return __q1a_raw(
        __get_records(Qry.get('Q1A_RAW_DATE').format(date=date)),
        date.isoformat(),
        request.args.get('xls') is not None
    )


@bp.route('/q1a/<int:y>/<int:m>/', methods=['GET'])
def q1a_raw_month(y: int, m: int):
    iy = int(y)
    im = int(m)
    return __q1a_raw(
        __get_records(Qry.get('Q1A_RAW_MONTH').format(y=iy, m=im)),
        "{:d}-{:02d}".format(iy, im),
        request.args.get('xls') is not None
    )


@bp.route('/q1a/<int:y>/', methods=['GET'])
def q1a_raw_year(y: int):
    return __q1a_raw(
        __get_records(Qry.get('Q1A_RAW_YEAR').format(y=int(y))),
        str(y),
        request.args.get('xls') is not None
    )


@bp.route('/q1a/table/', methods=['GET', 'POST'])
def q1a_table():
    form = forms.Q1ATableForm()
    data = []
    title = ""
    in_btc = False
    if form.validate_on_submit():
        qid = form.qid.data
        __update_cookie(COOKEY_FORM_QID, qid)
        date0 = form.date0.data
        __update_cookie(COOKEY_FORM_DATE0, date0)
        date1 = form.date1.data
        __update_cookie(COOKEY_FORM_DATE1, date1)
        data = __get_records(Qry.get('Q1A_X').format(qid=qid, date0=date0, date1=date1))
        title = f"qid={qid} for {date0}...{date1}"
        in_btc = qid in {4, 6}
    elif request.method == 'GET':
        if qid := __get_cookie(COOKEY_FORM_QID):
            form.qid.data = qid
        if date0 := __get_cookie(COOKEY_FORM_DATE0, datetime.date):
            form.date0.data = date0
        if date1 := __get_cookie(COOKEY_FORM_DATE1, datetime.date):
            form.date1.data = date1
    return render_template("q1a_table.html", form=form, title=title, data=data, in_btc=in_btc)


def __plt2svg() -> str:
    of = io.StringIO()
    plt.savefig(of, format='svg')
    return of.getvalue()


@bp.route('/q1a/2d/date/', methods=['GET', 'POST'])
def q1a_2d_date():
    def __mk_plot(__data: Iterable) -> str:
        x = []
        y = []
        for row in __data:
            x.append(row.d)
            y.append(row.val)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        return __plt2svg()
    form = forms.Q1A2DDatesForm()
    data = None
    if form.validate_on_submit():
        qid = form.qid.data
        rid = form.rid.data
        date0 = form.date0.data
        date1 = form.date1.data
        # percent = form.percent.data
        # in_btc = qid in {4, 6}
        title = f"qid={qid}, rid={rid} for {date0}...{date1}"
        src = __get_records(Qry.get('Q1A_2D_DATE').format(qid=qid, rid=rid, date0=date0, date1=date1))
        data = {'title': title, 'svg': __mk_plot(src)}
    return render_template("q1a_2d_date.html", form=form, data=data)


@bp.route('/q1a/2d/rid/', methods=['GET', 'POST'])
def q1a_2d_rid():
    def __mk_plot(__data: Iterable) -> str:
        x = []
        y = []
        for row in __data:
            x.append(row.rid)
            y.append(row.val)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        return __plt2svg()
    form = forms.Q1A2DRIDForm()
    data = None
    if form.validate_on_submit():
        qid = form.qid.data
        date0 = form.date0.data
        # percent = form.percent.data
        # in_btc = qid in {4, 6}
        title = f"qid={qid} for {date0}"
        src = __get_records(Qry.get('Q1A_2D_RID').format(qid=qid, date0=date0))
        data = {'title': title, 'svg': __mk_plot(src)}
    return render_template("q1a_2d_date.html", form=form, data=data)


@bp.route('/q2606/', methods=['GET', 'POST'])
def q2606():
    form = forms.Q2606Form()
    if form.validate_on_submit():
        date0 = form.date0.data
        __update_cookie(COOKEY_FORM_DATE0, date0)
        rid = form.rid.data
        __update_cookie(COOKEY_FORM_RID, rid)
        if num := form.num.data:
            __update_cookie(COOKEY_FORM_NUM, num)
        # return redirect(url_for('bceweb.q_index'))
        # print(date0, RID[rid][0], RID[rid][1], num)
        data = __get_records(Qry.get('Q2606').format(
            date0=date0.isoformat(),
            m_min=RID[rid-1][0],
            m_max=RID[rid-1][1],
            num=num or 22*10**6)
        )
        ofile = xlstore.q2606_csf(date0, data)
        ofile.seek(0)
        fname = f"q2606-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}.txt"
        return send_file(
            io.BytesIO(ofile.read().encode()),
            mimetype='text/plain',
            as_attachment=True,
            download_name=fname,
            attachment_filename=fname
        )
    elif request.method == 'GET':
        if date0 := __get_cookie(COOKEY_FORM_DATE0, datetime.date):
            form.date0.data = date0
        if rid := __get_cookie(COOKEY_FORM_RID):
            form.rid.data = rid
        if num := __get_cookie(COOKEY_FORM_NUM):
            form.num.data = num
    return render_template("q2606.html", form=form)
