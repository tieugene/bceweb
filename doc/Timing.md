# Timing

## 220420

Test queries `addr_*` @ `vout` vs `tail`.
Limits: 50 @ 2022-02-01..03-31 or 10k @ 2022-03-31 (`gt`)

Query    | vout| tail| %
---------|-----|-----|---
`btc_max`| 369 | 227 | 
`btc_min`| 366 | 215 | 
`cnt_max`| 379 | 226 | 
`cnt_min`| --- | 228 | 
`gt`     | 209 |  90 | 

## 220303
Test 4_tx_suco_tmp - count/sum via interim qid table.  
Stand: Alex, 2016-12-31 (bk 446017, tx 183758064..183759444)

- [x] mk table: 1'12" (13219096 rows)
- [x] +idx: 1'25" (+13")
- [x] +Addr_Num: 1'30" (+5") &check;
- [x] +Addr_Sum: 3'15" (+2') &check;
- [x] +Addr_Num_Active: 4'57 &check;
- [ ] mk_idx: 4'53"
- [x] +Vout_Num: 4'53" &check;
- [x] +Vout_Sum: 4'51"
- [x] +Vin_Sum: 4'53"
- [ ] +Vloop_Num: 4'52"

## 220301

Count/Sum by buratinity.
Stands:
- host002, 450k, Cut-off: 2016-12-31 (bk 446017, tx 183759444), 12M addrs:
  - txo/date:   40" ( 373620064 rows (  12"))
  - vout/tx:  4'40" ( 530923560 rows (3'35"))
- alex (700k), Cut-off: 2020-12-31 (bk 663886, tx 601532548), 33M addrs
  - txo/date: 1'33" ( 312140824 rows (   6"))
  - vout/tx:  2'59" (1850391428 rows (  45"))
  - vout/tx:  1'34" (tx=183759444)

## `refresh_bk_stat.sql`

Alex:

 k |  PR | Alex
---|----:|----:
100|  | 02:07:38
450|  | 07:00:00

## q\_addr\_x:
- PR: date=2016-12-01..2016-12-31, num=20/10^12
- Alex: date=2020-12-01..2020-12-31, num=20/10^12

Query   | PR.txo| PR.vo | Al.txo| Al.vo
--------|-------|-------|-------|------
btc_max | 01:26 | 11:21 | 02:33 | 10:14
btc_min | 01:26 | 09:02 | 02:34 | 05:13
cnt_max | 01:28 | 08:08 | 02:44 | 05:24
cnt_min | 01:29 | 11:15 | 02:43 | 05:24
gt      | 03:43 | 05:17 | 07:11 | 02:18
