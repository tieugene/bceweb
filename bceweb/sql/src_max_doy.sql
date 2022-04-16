-- Max date of year
SELECT MAX(DATE(datime)) FROM bk WHERE EXTRACT (YEAR FROM datime) = {year};
