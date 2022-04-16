-- Max month of year
SELECT MAX(EXTRACT (MONTH FROM datime)) FROM bk WHERE EXTRACT (YEAR FROM datime) = {year};