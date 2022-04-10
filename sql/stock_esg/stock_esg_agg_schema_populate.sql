-- populate stock table
COPY stock_esg_agg
FROM '/home/airflow/airflow/csv/stock_esg/aggregated_data.csv'
DELIMITER ',' 
CSV HEADER;