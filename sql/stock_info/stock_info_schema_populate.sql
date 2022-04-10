-- populate stock table
COPY stock_info
FROM '/home/airflow/airflow/csv/stock_info/stocks_info_transformed.csv'
DELIMITER ',' 
CSV HEADER;