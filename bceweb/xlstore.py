"""XLSX files store"""
# 1. std
import io
from enum import IntEnum
from typing import Optional, Iterable
# 2. 3rd
import xlsxwriter


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
    options = {'in_memory': True}
    xl_id = Store.new()
    like_file = io.BytesIO()
    workbook = xlsxwriter.Workbook(like_file, options)
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
