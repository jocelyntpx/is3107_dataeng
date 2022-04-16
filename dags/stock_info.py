from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
import os
import csv
import logging
import yahoo_fin.stock_info as si


from datetime import datetime, timedelta  
import datetime as dt
import numpy as np
import pandas as pd

#STI Index
tickers = ['C6L.SI','D05.SI','C52.SI','G13.SI','C38U.SI',
            'U11.SI','Y92.SI','N2IU.SI','S58.SI','F34.SI',
            'M44U.SI','Z74.SI','C09.SI','BS6.SI','V03.SI']


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

PROJECT_ID = "is3107-stocks-project"
DATASET_NAME = "stock_info"
CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
BUCKET_NAME = "is3107-stocks-analysis"
GS_PATH = "data/stock_info/"
TABLE_ARRAY = ["stock_info"]
TABLE_1 = "stock_info"
LOCATION = "asia-southeast1"


SCHEMA = [
    {"name": "Stock_Ticker", "type": "STRING", "mode": "REQUIRED"},
    {"name": "Enterprise_Value", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "EBITDA", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Revenue", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Forward_PE", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Market_Cap", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "PEG_Ratio", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Price_Book", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Price_Sales", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Trailing_PE", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "EV_Scale", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "MC_Scale", "type": "INTEGER", "mode": "NULLABLE"},
]

dag_id = "stock_info_google_cloud" 
DATASET = DATASET_NAME 
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")


SELECT_DATASET_QUERY = """SELECT * FROM {{ DATASET }}.{{ TABLE }}"""

####################################################
# 1. DEFINE PYTHON FUNCTIONS
####################################################

def fetch_stock_info_function(**kwargs): # <-- Remember to include "**kwargs" in all the defined functions 
    print('1 Fetching stock info ...')
    stocks_prices = []
    dow_stats = {}
    for ticker in tickers:
        temp = si.get_stats_valuation(ticker)
        temp = temp.iloc[:,:2]
        temp.columns = ["Attribute", "Recent"]
        dow_stats[ticker] = temp
    print('Completed \n\n')
    return dow_stats # <-- Input of function to concact prices

def stocks_info_concat_function(**kwargs): 
    print('2 Pulling stock_info to concatenate sub-lists to create a combined dataset + write to CSV file...')
    ti = kwargs['ti']
    dow_stats= ti.xcom_pull(task_ids='fetch_stock_info') # <-- xcom_pull is used to pull the stocks_prices list generated above
    combined_stats = pd.concat(dow_stats)
    combined_stats = combined_stats.reset_index().drop(columns=['level_1']).rename(columns={'level_0':'stock_ticker'})
    combined = combined_stats.pivot(index='stock_ticker', columns='Attribute', values='Recent').reset_index().reset_index(drop=True)
    combined.columns.name = None
    combined.rename(columns={'Enterprise Value': 'Enterprise_Value', 'Enterprise Value/EBITDA':'EV_EBITDA', 'Enterprise Value/Revenue': 'EV_Rev', 'Forward P/E':'Forward_PE','Market Cap (intraday)': 'Market_Cap', 'PEG Ratio (5 yr expected)': 'PEG_Ratio','Price/Book (mrq)': 'PB_Ratio', 'Price/Sales (ttm)': 'PS_Ratio', 'Trailing P/E': 'PE_Ratio'}, inplace=True)
    combined.to_csv('/home/airflow/airflow/csv/stock_info/stocks_info_cleaning.csv', index = False)
    print('DF Shape: ', combined.shape)
    print(combined.head(5))
    print('Completed \n\n')
    return combined


def stocks_info_transform_function(**kwargs): 
    print('3 Pulling concat stock_info for transformation')
    ti = kwargs['ti']
    combined= ti.xcom_pull(task_ids='stocks_info_concat') # <-- xcom_pull is used to pull the stocks_prices list generated above
    scale_dict = {
    'B': 9,
    'T': 12
    }
    
    combined['ev_scale'] = [x[-1] if not pd.isna(x) else np.nan for x in combined['Enterprise_Value']]
    combined['mc_scale'] = [x[-1] if not pd.isna(x) else np.nan for x in combined['Market_Cap']]
    combined['Enterprise_Value'] = [x[0:-1] if not pd.isna(x) else np.nan for x in combined['Enterprise_Value']]
    combined['Market_Cap'] = [x[0:-1] if not pd.isna(x) else np.nan for x in combined['Market_Cap']]
    combined['ev_scale'] = [scale_dict[x] if not pd.isna(x) else np.nan for x in combined['ev_scale']]
    combined['mc_scale'] = [scale_dict[x] if not pd.isna(x) else np.nan for x in combined['mc_scale']]
    combined.to_csv('/home/airflow/airflow/csv/stock_info/stocks_info_transformed.csv', index = False)

    print('DF Shape: ', combined.shape)
    print(combined.head(5))
    print('Completed \n\n')

############################################
#2. DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################

default_args = {
     'owner': 'airflow',
     'depends_on_past': False,
     'email': ['fxing@example.com'],
     'email_on_failure': False,
     'email_on_retry': False,
     'retries': 1
    }

dag = DAG( 'stocks_info_dag',
            default_args=default_args,
            description='Collect Stock Info For Analysis',
            catchup=False, 
            start_date= datetime(2020, 12, 23), 
            schedule_interval= '0 0 1 */3 *'  
          )  

##########################################
#3. DEFINE AIRFLOW OPERATORS
##########################################

start_pipeline = DummyOperator(
        task_id = 'start_pipeline',
        dag = dag
        )

fetch_stock_info = PythonOperator(task_id = 'fetch_stock_info', 
                                   python_callable = fetch_stock_info_function, 
                                   provide_context = True,
                                   dag= dag )

stocks_info_concat = PythonOperator(task_id = 'stocks_info_concat', 
                                   python_callable = stocks_info_concat_function, 
                                   provide_context = True,
                                   dag= dag )

stocks_info_transform= PythonOperator(task_id = 'stocks_info_transform', 
                                 python_callable = stocks_info_transform_function,
                                 provide_context = True,
                                 dag= dag)

create_stock_info_table = PostgresOperator(
        task_id="create_stock_info_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_info/stock_info_schema.sql",
)

populate_stock_info_table = PostgresOperator(
        task_id="populate_stocks_info_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_info/stock_info_schema_populate.sql",
)

trigger_bq = TriggerDagRunOperator(
    task_id="trigger_bq",
    trigger_dag_id="stock_info_google_cloud",
)

##########################################
#4. DEFINE OPERATORS HIERARCHY
##########################################

start_pipeline >> [fetch_stock_info,create_stock_info_table] >> stocks_info_concat >> stocks_info_transform >> populate_stock_info_table >> trigger_bq
