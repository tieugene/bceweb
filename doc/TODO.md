# TODO

*Test: 200k enough*

## common
- [ ] Query `txo:date0/1` &rArr; `vout:tx_id/..._in`
- [ ] Query tree:
  1. Year + Mon/Day
  1. Blocks (of date) (+scroll date)
  1. Block (+scroll blocks): stat
  1. tx (+scroll)
  1. vins/vouts (+scroll)
- [ ] remove blueprint
- [ ] NamedTupleConnection &sum;

## src_
*(None)*

## q_
- [ ] unification:
  - [x] num, date0, date1 (addr_*_* x4; num=qty (10..100))
  - [x] num, date1 (addr_gt; num=$ (1G+))
  - [ ] num, date0, date1, alist (alist_*_* x4; num=$/%)
  - [ ] date0, date1, alist (alist_moves)
- [ ] alist:
  - CSV
  - multicolumn text
  - checkboxed
  - upload
- [ ] don't forget wtforms.DecimalField()

## UI
- [ ] permanent vertical menu

## Maintain
- [ ] setup.py
- [ ] bceweb.spec

## Future
- [ ] xlsx: autoclean
- [ ] xlsx as template (&lt; flat xml)
- [ ] mobile version
- [ ] parametered sqls

## misc
- https://pythonru.com/uroki/1-vvedenie-vo-flask
- [RTFM](https://jinja.palletsprojects.com/en/3.0.x/templates/)
