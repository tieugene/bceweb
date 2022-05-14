#!/usr/bin/env python3
"""
Test of plotting 3D charts of q1a queries
SQL: SELECT d, qid, rid, val FROM t_1a_date WHERE date_part( 'year', d ) = 2022 ORDER BY d, qid, rid;
"""
import sys
from typing import TextIO
from datetime import date
import csv
# import pprint
# import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import numpy as np


def __load(infile: TextIO, qid: int, rid: int) -> list[tuple[date, int]]:
    """Load data from csv file.
    :param infile: Opened file
    :return: List of dates data [date, r1, ..., r10]
    """
    data: list = []
    reader = csv.reader(infile, dialect=csv.excel_tab())
    next(reader, None)  # skip header
    for irow in reader:
        if int(irow[1]) == qid and int(irow[2]) == rid:
            data.append((date.fromisoformat(irow[0]), int(irow[3])))
    return data


def __plot(data: list[tuple[date, int]]):
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    plt.show()


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <qid:int> <rid:int>")
        sys.exit(1)
    with open("_csv/2022.csv", 'rt') as infile:
        data = __load(infile, int(sys.argv[1]), int(sys.argv[2]))
        __plot(data)


if __name__ == '__main__':
    main()
