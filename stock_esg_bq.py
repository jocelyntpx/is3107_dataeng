"""
Example Airflow DAG for Google BigQuery service.
"""
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
DATASET_NAME = "stock_esg"
CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
BUCKET_NAME = "is3107-stocks-analysis"
GS_PATH = "data/stock_esg/"
TABLE_ARRAY_1 = ["stock_esg"]
TABLE_ARRAY_2 = ["stock_esg_agg"]
TABLE_1 = "stock_esg"
TABLE_2 = "stock_esg_agg"
LOCATION = "asia-southeast1"

SCHEMA_1 = [
    {"name": "Stock_Ticker", "type": "STRING", "mode": "REQUIRED"},
    {"name": "Environment_Score", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Esg_Performance", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Governance_Score", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Peer_Count", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Peer_Group", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Social_Score", "type": "FLOAT64", "mode": "NULLABLE"},
]

SCHEMA_2 = [
    {"name": "Peer_Group", "type": "STRING", "mode": "REQUIRED"},
    {"name": "Environment_Score_Avg", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Governance_Score_Avg", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "Social_Score_Avg", "type": "FLOAT64", "mode": "NULLABLE"},
]

dag_id = "stock_esg_google_cloud_dag" 
DATASET = DATASET_NAME 
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")

SELECT_DATASET_QUERY = """SELECT * FROM {{ DATASET }}.{{ TABLE }}"""

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
            schema_fields=SCHEMA_1,
            location=LOCATION,
            bigquery_conn_id=CONN_ID,             
            google_cloud_storage_conn_id=CONN_ID,
        )

        create_table_2 = BigQueryCreateEmptyTableOperator(
            task_id="create_table_2",
            dataset_id=DATASET,
            table_id=TABLE_2,
            schema_fields=SCHEMA_2,
            location=LOCATION,
            bigquery_conn_id=CONN_ID,             
            google_cloud_storage_conn_id=CONN_ID,
        )

        load_staging_dataset = DummyOperator(
            task_id = 'load_staging_dataset',
        )   

        Postgres_To_GCS1 = PythonOperator(
            task_id="Postgres_To_GCS1",
            python_callable=postgres_to_gcs.Postgres_To_GCS1,
            op_kwargs = {'TABLE_ARRAY_1':TABLE_ARRAY_1,
                        'GS_PATH':GS_PATH},
        )

        Postgres_To_GCS2 = PythonOperator(
            task_id="Postgres_To_GCS2",
            python_callable=postgres_to_gcs.Postgres_To_GCS2,
            op_kwargs = {'TABLE_ARRAY_2':TABLE_ARRAY_2,
                        'GS_PATH':GS_PATH},
        )
        
        push_to_bigquery_1= PythonOperator(task_id = 'push_to_bigquery_1', 
                                 python_callable = push_to_bq.push_to_bigquery1,
                                 op_kwargs = {'TABLE_ARRAY_1':TABLE_ARRAY_1,
                                                'DATASET_NAME':DATASET_NAME,
                                                'TABLE_1':TABLE_1,
                                                'PARTS': 2},
                                 provide_context = True,
        )

        push_to_bigquery_2= PythonOperator(task_id = 'push_to_bigquery_2', 
                                 python_callable = push_to_bq.push_to_bigquery2,
                                 op_kwargs = {'TABLE_ARRAY_2':TABLE_ARRAY_2,
                                                'DATASET_NAME':DATASET_NAME,
                                                'TABLE_2':TABLE_2,
                                                'PARTS': 2},
                                 provide_context = True,
        )
        
        finish_pipeline = DummyOperator(
            task_id = 'finish_pipeline',
        )  

create_dataset >> [create_table_1,create_table_2] >>load_staging_dataset >> [Postgres_To_GCS1,Postgres_To_GCS2,push_to_bigquery_1,push_to_bigquery_2]  >> finish_pipeline
