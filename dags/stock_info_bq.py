import os
from datetime import datetime
import csv
import logging

from airflow import models
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
)

from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

import sys
sys.path.append('/home/airflow/airflow/scripts')
import postgres_to_gcs
import push_to_bq

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

PROJECT_ID = "is3107-stocks-project"
DATASET_NAME = "stock_info"
CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
BUCKET_NAME = "is3107-project-stock-analysis"
GS_PATH = "data/stock_info/"
TABLE_ARRAY_1 = ["stock_info"]
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
    {"name": "EV_Scale", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "MC_Scale", "type": "INTEGER", "mode": "NULLABLE"},
]


dag_id = "stock_info_google_cloud" 
DATASET = DATASET_NAME 
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")

SELECT_DATASET_QUERY = """SELECT * FROM {{ DATASET }}.{{ TABLE }}"""


############################################
#2. DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################

with models.DAG(
    dag_id,
    schedule_interval='@once',  # Override to match your needs
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
     user_defined_macros={"DATASET": DATASET, "TABLE": TABLE_1},
    ) as dag_with_locations:

        create_dataset = BigQueryCreateEmptyDatasetOperator(
            task_id="create-dataset",
            dataset_id=DATASET,
            location=LOCATION,
            bigquery_conn_id=CONN_ID,             
            gcp_conn_id=CONN_ID,
        )

        create_table_1 = BigQueryCreateEmptyTableOperator(
            task_id="create_table_1",
            dataset_id=DATASET,
            table_id=TABLE_1,
            schema_fields=SCHEMA,
            location=LOCATION,
            bigquery_conn_id=CONN_ID,             
            google_cloud_storage_conn_id=CONN_ID,
        )

        postgresToGCS1 = PythonOperator(
            task_id="PostgresToGCS1",
            python_callable=postgres_to_gcs.Postgres_To_GCS1,
            op_kwargs = {'TABLE_ARRAY_1':TABLE_ARRAY_1,
                        'GS_PATH':GS_PATH},
        )
        
        push_to_bigquery= PythonOperator(task_id = 'push_to_bigquery', 
                                 python_callable = push_to_bq.push_to_bigquery1,
                                 provide_context = True,
                                 op_kwargs = {'TABLE_ARRAY_1':TABLE_ARRAY_1,
                                                'DATASET_NAME':DATASET_NAME,
                                                'TABLE_1':TABLE_1,
                                                'PARTS': 2},
        )

        finish_pipeline = DummyOperator(
        task_id = 'finish_pipeline'
        )
        

create_dataset >> create_table_1 >> [postgresToGCS1,push_to_bigquery] >> finish_pipeline