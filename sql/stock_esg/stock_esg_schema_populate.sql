-- populate stock table
COPY stock_esg
FROM '/home/airflow/airflow/csv/stock_esg/stocks_esg.csv'
DELIMITER ',' 
CSV HEADER;