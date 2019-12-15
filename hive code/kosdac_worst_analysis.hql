SELECT stock.company_name,stock.date_yyyy_mm_dd,AVG(stock.now_price)
FROM stock LEFT SEMI JOIN kosdac_worst_top5 on (stock.company_name = kosdac_worst_top5.worst_company_name)
GROUP BY stock.company_name,stock.date_yyyy_mm_dd