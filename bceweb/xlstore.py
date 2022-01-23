"""XLSX files store"""
# 1. std
import os
from typing import Optional
# 2. 3rd
from flask import current_app
import xlsxwriter


class Store:
    __counter: int = 0

    @staticmethod
    def __base():
        return current_app.config.get('XLSTORE')

    @staticmethod
    def __clean():
        """Clean cache dir before usage"""
        with os.scandir(Store.__base()) as itr:
            for entry in itr:
                if not entry.is_file():
                    os.remove(entry.path)

    @staticmethod
    def path(xl_id: int):
        return os.path.join(Store.__base(), str(xl_id)+'.xlsx')

    @staticmethod
    def new() -> int:
        """Create new filename.
        :return: Path of new file
        """
        if Store.__counter == 0:
            Store.__clean()
        Store.__counter += 1
        return Store.__counter

    @staticmethod
    def get(xl_id: int) -> Optional[str]:
        """Get file path if exists.
        :param xl_id: File ID to get
        :return: Path of prev created XLSX file
        """
        path = Store.path(xl_id)
        if os.path.isfile(path):
            return path


def mk_xlsx(meta: dict, head: tuple, data) -> int:
    """Create xlsx file.
    :return: New file id
    :todo: cell_format = workbook.add_format({'bold': True, 'font_name': 'Courier', 'align': 'right', 'num_format': '$#,##0.00'})
    """
    # 'strings_to_numbers': True
    options = {'in_memory': True}
    xl_id = Store.new()
    workbook = xlsxwriter.Workbook(Store.path(xl_id))
    workbook.set_properties(meta)  # 'title', 'subject', 'create[d]', comments)
    worksheet = workbook.add_worksheet()
    # formats
    head_format = workbook.add_format({'bold': True, 'align': 'center'})
    # header
    worksheet.write_row(0, 0, head, head_format)
    worksheet.freeze_panes(1, 0)
    # data
    for row, item in enumerate(data):
        worksheet.write_row(row+1, 0, item)
    workbook.close()
    return xl_id
