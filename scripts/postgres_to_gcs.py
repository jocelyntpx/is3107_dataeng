
import os
import csv
import logging
from datetime import datetime

from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook 

CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
BUCKET_NAME = "is3107-stock-analysis"
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")

def Postgres_To_GCS1(TABLE_ARRAY_1,GS_PATH):
    for table in TABLE_ARRAY_1:
        gcs_hook = GoogleCloudStorageHook(CONN_ID)
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("select * from " + table)
        result = cursor.fetchall()
        with open(table +'.csv', 'w') as fp:
            a = csv.writer(fp, quoting = csv.QUOTE_MINIMAL, delimiter = ',')
            a.writerow([i[0] for i in cursor.description])
            a.writerows(result)
        logging.info("Uploading to bucket, " + table + ".csv")
        gcs_hook.upload(BUCKET_NAME, GS_PATH +table + "_pg_" +INSERT_DATE+ ".csv", table + ".csv")

def Postgres_To_GCS2(TABLE_ARRAY_2,GS_PATH):
    for table in TABLE_ARRAY_2:
        gcs_hook = GoogleCloudStorageHook(CONN_ID)
        pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("select * from " + table)
        result = cursor.fetchall()
        with open(table +'.csv', 'w') as fp:
            a = csv.writer(fp, quoting = csv.QUOTE_MINIMAL, delimiter = ',')
            a.writerow([i[0] for i in cursor.description])
            a.writerows(result)
        logging.info("Uploading to bucket, " + table + ".csv")
        gcs_hook.upload(BUCKET_NAME, GS_PATH +table + "_pg_" +INSERT_DATE+ ".csv", table + ".csv")
