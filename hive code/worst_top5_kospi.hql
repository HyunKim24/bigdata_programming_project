SELECT worst_top5.company_name 
FROM(SELECT kospi.company_name,kospi.now_price
	  FROM(SELECT stock.company_name,stock.date_yyyy_mm_dd,stock.time,stock.now_price
			  FROM stock
			  WHERE stock.market == '코스피') AS kospi
	  WHERE kospi.date_yyyy_mm_dd == '2019-12-10' and kospi.time == '09:30'
	  ORDER BY kospi.now_price ASC LIMIT 5) AS worst_top5