import os
import csv
import logging
from datetime import datetime,timedelta

from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook 
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
PROJECT_ID = "is3107-stocks-project"
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")
PREVIOUS_DAY = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

def chunk(l,n):
  d,r = divmod(len(l),n) 
  for i in range (n):
    si= (d+1)* (i if i<r else r) + d*(0 if i < r else i-r)
    yield l[si:si+(d+1 if i < r else d)]


def push_to_bigquery1(TABLE_ARRAY_1, DATASET_NAME, TABLE_1, PARTS):
    for table in TABLE_ARRAY_1:
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        print(INSERT_DATE,PREVIOUS_DAY,table)
        if DATASET_NAME == "stock_price":
            cursor.execute("select * from " + table)
            # query = f"""
            #     SELECT * FROM {table}
            #     WHERE {table}.Date BETWEEN '{PREVIOUS_DAY}' AND '{INSERT_DATE}';
            # """
            # cursor.execute(query)
        else :
            cursor.execute("select * from " + table)
        result = cursor.fetchall()
    print(result)
    lst = list(chunk(result, PARTS))
    for res in lst:
        bq_hook = BigQueryHook()
        bq_hook.insert_all(project_id=PROJECT_ID, dataset_id=DATASET_NAME, table_id=TABLE_1, rows = res)

def push_to_bigquery2(TABLE_ARRAY_2,DATASET_NAME,TABLE_2, PARTS):
    for table in TABLE_ARRAY_2:
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("select * from " + table)
        result = cursor.fetchall()
    lst = list(chunk(result, PARTS))
    for res in lst:
        bq_hook = BigQueryHook()
        bq_hook.insert_all(project_id=PROJECT_ID, dataset_id=DATASET_NAME, table_id=TABLE_2, rows = res)
