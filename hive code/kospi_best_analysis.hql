SELECT stock.company_name,stock.date_yyyy_mm_dd,AVG(stock.now_price)
FROM stock LEFT SEMI JOIN kospi_best_top5 on (stock.company_name = kospi_best_top5.best_company_name)
GROUP BY stock.company_name,stock.date_yyyy_mm_dd