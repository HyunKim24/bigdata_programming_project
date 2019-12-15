SELECT best_top5.company_name 
FROM(SELECT kosdac.company_name,kosdac.now_price
	  FROM(SELECT stock.company_name,stock.date_yyyy_mm_dd,stock.time,stock.now_price
			  FROM stock
			  WHERE stock.market == '코스닥') AS kosdac
	  WHERE kosdac.date_yyyy_mm_dd == '2019-12-10' and kosdac.time == '09:30'
	  ORDER BY kosdac.now_price DESC LIMIT 5) AS best_top5
