DROP TABLE stock;
CREATE TABLE IF NOT EXISTS stock(
  no INT,
  date_yyyy_mm_dd STRING, 
  time STRING,
  market STRING,
  company_name STRING,
  now_price INT,
  per_yesterday INT,
  in_decrease STRING,
  per_value INT,
  market_cap INT,
  listed_stock INT,
  foreing_rate DOUBLE,
  trading_volume INT,
  per DOUBLE,
  roe DOUBLE
)
row format delimited fields terminated BY ',' lines terminated BY '\n'
tblproperties("skip.header.line.count"="1");

LOAD DATA INPATH '/user/maria_dev/stock/final_dataset.csv' OVERWRITE INTO TABLE stock;

SELECT * FROM stock LIMIT 30;
  