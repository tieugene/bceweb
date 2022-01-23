# TODO

- [RTFM](https://jinja.palletsprojects.com/en/3.0.x/templates/)

## common
*(None)*

## src_
*(None)*

## q_
- [ ] unification:
  - [x] num, date0, date1 (addr_*_* x4; num=qty (10..100))
  - [x] num, date1 (addr_gt; num=$ (1G+))
  - [ ] num, date0, date1, alist (alist_*_* x4; num=$/%)
  - [ ] date0, date1, alist (alist_moves)
- [ ] XLSX:
  - [ ] btc
  - [ ] format cells:
    - [ ] mono
    - [ ] right
    - [ ] thousands
- [ ] don't forget wtforms.DecimalField()

## UI
- [ ] permanent vertical menu

## Maintain
- [ ] setup.py
- [ ] bceweb.spec

## Future
- [ ] xlsx as template (&lt; flat xml)
- [ ] xlsx cache as BytesIO()
- [ ] mobile version
- [ ] parametered sqls
