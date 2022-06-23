"""XLSX files store"""
# 1. std
import io
from datetime import date, datetime
from enum import IntEnum
from typing import Optional, Iterable
# 2. 3rd
import xlsxwriter

OPTIONS = {'in_memory': True}


class ECellType(IntEnum):
    BTC = 1
    Date = 2


class Store:
    __counter: int = 0
    __store: dict[int, bytes] = {}

    @staticmethod
    def new() -> int:
        """Create new filename.
        :return: Path of new file
        """
        Store.__counter += 1
        return Store.__counter

    @staticmethod
    def set(xl_id: int, data: io.BytesIO):
        """Save in-memory 'file' to store
        :todo: autoclean
        """
        Store.__store[xl_id] = data.getvalue()

    @staticmethod
    def get(xl_id: int) -> Optional[bytes]:
        """Get file path if exists.
        :param xl_id: File ID to get
        :return: Path of prev created XLSX file
        """
        return Store.__store.get(xl_id)


def mk_xlsx(meta: dict, head: tuple, data: Iterable, col_fmt: dict[int: ECellType] = {}) -> int:
    """Create xlsx file.
    :return: New file id
    """
    # 'strings_to_numbers': True
    xl_id = Store.new()
    like_file = io.BytesIO()
    workbook = xlsxwriter.Workbook(like_file, OPTIONS)
    workbook.set_properties(meta)  # 'title', 'subject', 'create[d]', comments)
    worksheet = workbook.add_worksheet()
    # formats
    head_format = workbook.add_format({'bold': True, 'align': 'center'})
    btc_format = workbook.add_format({'font_name': 'Courier', 'num_format': '# ##0.00000000'})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    # header
    worksheet.write_row(0, 0, head, head_format)
    worksheet.freeze_panes(1, 0)
    # data
    for row, data_row in enumerate(data):
        for col, cell in enumerate(data_row):
            if cell is not None:
                if fmt := col_fmt.get(col):
                    if fmt == ECellType.BTC:
                        worksheet.write_number(row + 1, col, cell/100000000, btc_format)
                    elif fmt == ECellType.Date:
                        worksheet.write_datetime(row + 1, col, cell, date_format)
                else:
                    worksheet.write(row + 1, col, cell)
    workbook.close()
    Store.set(xl_id, like_file)
    return xl_id


def q1a(data: Iterable) -> bytes:
    """
    Make xlsx with Q1A's 'table' data.
    :param data: recordset of (d:date, qid:int, rid:int, val:bigint)
    :return:
    """
    meta = {'title': "Q1A", 'subject': "Subject", 'created': date.today(), 'comments': ''}
    head = ('date', 'rid1', 'rid2', 'rid3', 'rid4', 'rid5', 'rid6', 'rid7', 'rid8', 'rid9', 'rid10', 'rid11')
    like_file = io.BytesIO()
    workbook = xlsxwriter.Workbook(like_file, OPTIONS)
    workbook.set_properties(meta)  # 'title', 'subject', 'create[d]', comments)
    # formats
    head_format = workbook.add_format({'bold': True, 'align': 'center'})
    # btc_format = workbook.add_format({'font_name': 'Courier', 'num_format': '# ##0.00000000'})
    num_format = workbook.add_format({'font_name': 'Courier', 'num_format': '0'})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    # prepare worksheets
    worksheet = []
    for i in range(6):
        ws = workbook.add_worksheet(f"qid{i+1}")
        # header
        ws.write_row(0, 0, head, head_format)
        ws.freeze_panes(1, 1)
        worksheet.append(ws)
    # data
    d = None
    orow = 0
    for irow in data:
        if irow[0] != d:
            d = irow[0]
            orow += 1
            for i in range(6):
                worksheet[i].write_datetime(orow, 0, d, date_format)
        worksheet[irow[1]-1].write_number(orow, irow[2], irow[3], num_format)
    workbook.close()
    return like_file.getvalue()


def q2606_csf(d: date, data: Iterable, crlf: bool) -> io.StringIO:
    """
    Make like-CSV file for Wolfram on given data
    :param d: date start from
    :param data: queryset
    :param crlf: end address record with CR/LF
    :return: file-like object
    """

    def __out_vout(_d: date, _row: list, _file: io.StringIO):
        """Print one vout
        :param _d: date from
        :param _row: [money, d0, d1]
        :param _file: file to print to
        """

        def __prn(m: int, __d: datetime, __file: io.StringIO):
            print(",{%.3f,%s}" % (m / 100000000, __d.strftime("%y,%m,%d,%H,%M")), end='', file=__file)

        if _row[1].date() >= _d:
            __prn(_row[0], _row[1], _file)
        if _row[2] is not None:
            __prn(-_row[0], _row[2], _file)

    like_file = io.StringIO()
    addr = None
    eol = '\n' if crlf else ''
    rs = ''  # record separator (between addrs)
    print("{", end='', file=like_file)
    for row in data:
        a_id = row[0]
        if a_id != addr:
            print("%s{%s" % (rs, row[1]), end='', file=like_file)
            addr = a_id
            if not rs:
                rs = "},%s" % eol
        __out_vout(d, row[2:], like_file)
    print("}}", file=like_file)
    return like_file
