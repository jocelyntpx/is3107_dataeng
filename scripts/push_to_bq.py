import os
import csv
import logging
from datetime import datetime

from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook 
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
PROJECT_ID = "united-planet-344907"

def push_to_bigquery1(TABLE_ARRAY_1, DATASET_NAME, TABLE_1):
    for table in TABLE_ARRAY_1:
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("select * from " + table)
        result = cursor.fetchall()
    bq_hook = BigQueryHook()
    bq_hook.insert_all(project_id=PROJECT_ID, dataset_id=DATASET_NAME, table_id=TABLE_1, rows = result)

def push_to_bigquery2(TABLE_ARRAY_2,DATASET_NAME,TABLE_2):
    for table in TABLE_ARRAY_2:
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("select * from " + table)
        result = cursor.fetchall()
    bq_hook = BigQueryHook()
    bq_hook.insert_all(project_id=PROJECT_ID, dataset_id=DATASET_NAME, table_id=TABLE_2, rows = result)
