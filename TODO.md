# TODO

- [RTFM](https://jinja.palletsprojects.com/en/3.0.x/templates/)

## common
- [ ] on-demand DB connection
- [ ] 

## src_
- [ ] parametered sqls
- [ ] format money (thousands separator)

## q_
- [ ] XLSX export:
  - [ ] Select engine:
    - [ ] [python3-xlsxwriter](https://pypi.python.org/pypi/XlsxWriter) (2007+)
    - [ ] python3-openpyxl (2010+)
  - [ ] Hot download:
    - Store data tmp (q_name_num_date0_date1 | unixstime)
    - Don't create until 'Download'
    - Create from tmp on 'XLSX' pressed
- [ ] add timestamp + timer 

## Info
- [ ] services status
  - [ ] bitcoind
  - [ ] db
- [ ] DBs info:
  - [ ] bitcoind height
  - [ ] DB main (blocks, dates)
  - [ ] txo

## UI
- [ ] permanent vertical menu
- [ ] mobile version

## Maintain
- [ ] setup.py
- [ ] .spec
