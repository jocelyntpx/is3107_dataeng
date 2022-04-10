-- populate stock table
COPY stock_price
FROM '/home/airflow/airflow/csv/stock_price/stocks_price.csv'
DELIMITER ',' 
CSV HEADER;