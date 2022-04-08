from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
import os
import csv
import logging
import yfinance as yf
from datetime import datetime, timedelta  
import datetime as dt
import numpy as np
import pandas as pd

#STI Index
tickers = ['C6L.SI','D05.SI','C52.SI','G13.SI','C38U.SI',
            'U11.SI','Y92.SI','N2IU.SI','S58.SI','F34.SI',
            'M44U.SI','Z74.SI','C09.SI','BS6.SI','V03.SI']

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

####################################################
# 1. DEFINE PYTHON FUNCTIONS
####################################################

def fetch_stock_esg_function(**kwargs): # <-- Remember to include "**kwargs" in all the defined functions 
    print('1 Fetching stock esg information and putting in to csv data ')
    new_df = pd.DataFrame()
    for i in tickers:
        try:
            df = yf.Ticker(i).sustainability.reset_index()
            df = df.loc[df[df.columns[0]].isin(['esgPerformance', 'environmentScore', 'socialScore', 'governanceScore', 'peerGroup', 'peerCount'])]
            df['stock_ticker'] = i
            df = df.pivot(index = 'stock_ticker', columns=df.columns[0], values='Value').reset_index()
            df = df[['stock_ticker','environmentScore','esgPerformance','governanceScore','peerCount','peerGroup','socialScore']].reset_index(drop=True)
            new_df = pd.concat([new_df,df])
        except:
            print('No data obtained')

    new_df['esgPerformance'] = [x.split('_')[0] if not pd.isna(x) else np.nan for x in new_df['esgPerformance']]
    new_df['environmentScore'] = new_df['environmentScore'].astype('float')
    new_df['socialScore'] = new_df['environmentScore'].astype('float')
    new_df['governanceScore'] = new_df['environmentScore'].astype('float')
    new_df.set_index('stock_ticker')
    new_df.to_csv('/home/airflow/airflow/csv/stock_esg/stocks_esg.csv', index = False)
    return new_df  # <-- This list is the output of the fetch_prices_function and the input for the functions below
    print('Completed \n\n')

def aggragate_env_score_function(**kwargs):
    print('2 grouping environment score  ')
    ti = kwargs['ti']
    new_df= ti.xcom_pull(task_ids='fetch_stock_esg')
    print(new_df)
    agg_env = new_df.groupby('peerGroup')[['environmentScore']].mean()
    return agg_env

def aggragate_gov_score_function(**kwargs):
    print('2 grouping governance score  ')
    ti = kwargs['ti']
    new_df= ti.xcom_pull(task_ids='fetch_stock_esg')
    agg_gov = new_df.groupby('peerGroup')[['governanceScore']].mean()
    return agg_gov

def aggragate_soc_score_function(**kwargs):
    print('2 grouping social score  ')
    ti = kwargs['ti']
    new_df= ti.xcom_pull(task_ids='fetch_stock_esg')
    print(new_df)
    agg_soc = new_df.groupby('peerGroup')[['socialScore']].mean()
    return agg_soc

def combine_data_function(**kwargs):
    print('3 combining data...  ')
    ti = kwargs['ti']
    agg_env= ti.xcom_pull(task_ids='aggragate_env_score_task')
    agg_gov= ti.xcom_pull(task_ids='aggragate_gov_score_task')
    agg_soc= ti.xcom_pull(task_ids='aggragate_soc_score_task')
    agg = pd.concat([agg_env, agg_gov, agg_soc], axis=1)

    agg = agg.reset_index()
    agg.columns.name=None
    agg.columns = agg.columns +'_' +'avg'
    agg.rename(columns={'peerGroup_avg': 'peerGroup'}, inplace=True)
    agg.to_csv('/home/airflow/airflow/csv/stock_esg/aggregated_data.csv', index = False)


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

dag = DAG( 'stocks_esg_dag',
            default_args=default_args,
            description='Collect Stock ESG Info For Analysis',
            catchup=False, 
            start_date= datetime(2020, 12, 23), 
            schedule_interval= '0 * * * *'  
          )  

##########################################
#3. DEFINE AIRFLOW OPERATORS
##########################################

start_pipeline = DummyOperator(
        task_id = 'start_pipeline',
        dag = dag
        )

fetch_stock_esg = PythonOperator(task_id = 'fetch_stock_esg', 
                                   python_callable = fetch_stock_esg_function, 
                                   provide_context = True,
                                   dag= dag )

create_stock_esg_table = PostgresOperator(
        task_id="create_stock_esg_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_esg/stock_esg_schema.sql",
)

create_stock_esg_agg_table = PostgresOperator(
        task_id="create_stock_esg_agg_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_esg/stock_esg_agg_schema.sql",
)

populate_stocks_esg_table = PostgresOperator(
        task_id="populate_stocks_esg_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_esg/stock_esg_schema_populate.sql",
)

calculate_env_avg = PythonOperator(task_id = 'aggragate_env_score_task', 
                                   python_callable = aggragate_env_score_function, 
                                   provide_context = True,
                                   dag= dag )
                
calculate_gov_avg = PythonOperator(task_id = 'aggragate_gov_score_task', 
                                   python_callable = aggragate_gov_score_function, 
                                   provide_context = True,
                                   dag= dag )

calculate_soc_avg = PythonOperator(task_id = 'aggragate_soc_score_task', 
                                   python_callable = aggragate_soc_score_function, 
                                   provide_context = True,
                                   dag= dag )         

combine_agg_data = PythonOperator(task_id = 'combine_agg_data', 
                                   python_callable = combine_data_function, 
                                   provide_context = True,
                                   dag= dag )  

populate_stocks_esg_agg_table = PostgresOperator(
        task_id="populate_stocks_esg_agg_table",
        postgres_conn_id="postgres_user",
        sql="sql/stock_esg/stock_esg_agg_schema_populate.sql",
)

trigger_bq = TriggerDagRunOperator(
    task_id="trigger_bq",
    trigger_dag_id="stock_esg_google_cloud_dag",
)

##########################################
#4. DEFINE OPERATORS HIERARCHY
##########################################

start_pipeline >> [fetch_stock_esg,create_stock_esg_table,create_stock_esg_agg_table] >> populate_stocks_esg_table 

fetch_stock_esg >> [calculate_env_avg,calculate_gov_avg,calculate_soc_avg] >> combine_agg_data >> populate_stocks_esg_agg_table >> trigger_bq