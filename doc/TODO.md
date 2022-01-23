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
- [ ] XLSX: format
  - [ ] thousands
  - [ ] mono
  - [ ] center on point
  - [ ] worksheet.freeze_panes()
- [ ] don't forget wtforms.DecimalField()
- Idea: xlsx as template

## UI
- [ ] permanent vertical menu

## Maintain
- [ ] setup.py
- [ ] bceweb.spec

## Future
- [ ] xlsx cache as BytesIO()
- [ ] mobile version
- [ ] parametered sqls
