from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
import os
import csv
import logging

from datetime import datetime, timedelta  
import numpy as np
import pandas as pd
import yfinance as yf


#STI Index
tickers = ['C6L.SI','D05.SI','C52.SI','G13.SI','C38U.SI',
            'U11.SI','Y92.SI','N2IU.SI','S58.SI','F34.SI',
            'M44U.SI','Z74.SI','C09.SI','BS6.SI','V03.SI'] 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

PROJECT_ID = "united-planet-344907"
DATASET_NAME = "stock_price"
CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
BUCKET_NAME = "is3107-stock-analysis"
GS_PATH = "data/stock_price/"
TABLE_ARRAY = ["stock_price"]
TABLE_1 = "stock_price_table"
LOCATION = "asia-southeast1"

SCHEMA = [
    {"name": "Date", "type": "DATE", "mode": "REQUIRED"},
    {"name": "Open", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "High", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Low", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Close", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Adj_Close", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Volume", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "Log_Return", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Pct_Return", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Stock_Ticker", "type": "STRING", "mode": "NULLABLE"},
]

dag_id = "stock_price_google_cloud" 
DATASET = DATASET_NAME 
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")

PREVIOUS_WEEK = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

SELECT_DATASET_QUERY = """SELECT * FROM {{ DATASET }}.{{ TABLE }}"""


####################################################
# 1. DEFINE PYTHON FUNCTIONS
####################################################

def fetch_prices_function(**kwargs): # <-- Remember to include "**kwargs" in all the defined functions 
    print('1 Fetching stock prices, remove duplicates and calcualting stock analysis ...')
    stocks_prices = []
    for i in tickers:
        prices = yf.download(i, start = PREVIOUS_WEEK)
        prices = prices.reset_index()
        prices['Log Returns'] = np.log(prices['Adj Close']/prices['Adj Close'].shift(1))
        prices['Pct Returns'] = np.exp(prices['Log Returns']) - 1
        prices['stock_ticker'] = i
        prices = prices.dropna(axis=0, how='any')
        stocks_prices.append(prices)
    return stocks_prices  # <-- This list is the output of the fetch_prices_function and the input for the functions below
    print('Completed \n\n')

 
def stocks_price_concat_function(**kwargs): 
    print('2 Pulling stocks_prices to concatenate sub-lists to create a combined dataset + write to CSV file...')
    ti = kwargs['ti']
    stocks_prices = ti.xcom_pull(task_ids='fetch_prices_task') # <-- xcom_pull is used to pull the stocks_prices list generated above
    stock_plots_data = pd.concat(stocks_prices, ignore_index = True)
    stock_plots_data.to_csv('/home/airflow/airflow/csv/stock_price/stocks_price.csv', index = False)

    print('DF Shape: ', stock_plots_data.shape)
    print(stock_plots_data.head(5))
    print('Completed \n\n')

############################################
#2. DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################

default_args = {
     'owner': 'fxing',
     'depends_on_past': False,
     'email': ['fxing@example.com'],
     'email_on_failure': False,
     'email_on_retry': False,
     'retries': 1
    }

dag = DAG( 'stocks_price_analysis',
            default_args=default_args,
            description='Collect Stock Prices For Analysis',
            catchup=False, 
            start_date= datetime(2020, 12, 23), 
            schedule_interval= '0 0 * * 1-5'  
          )  

##########################################
#3. DEFINE AIRFLOW OPERATORS
##########################################

start_pipeline = DummyOperator(
        task_id = 'start_pipeline',
        dag = dag
        )

fetch_prices_task = PythonOperator(task_id = 'fetch_prices_task', 
                                   python_callable = fetch_prices_function, 
                                   provide_context = True,
                                   dag= dag )

stocks_price_concat_task= PythonOperator(task_id = 'stocks_price_concat_task', 
                                 python_callable = stocks_price_concat_function,
                                 provide_context = True,
                                 dag= dag)


create_stock_table = PostgresOperator(
        task_id="create_stock_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_price/stock_schema.sql",
)

populate_stock_table = PostgresOperator(
        task_id="populate_stocks_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_price/stock_schema_populate.sql",
)

trigger_bq = TriggerDagRunOperator(
    task_id="trigger_bq",
    trigger_dag_id="stock_price_google_cloud",
)

##########################################
#4. DEFINE OPERATORS HIERARCHY
##########################################
start_pipeline >> [fetch_prices_task,create_stock_table] >> stocks_price_concat_task >> populate_stock_table >> trigger_bq
