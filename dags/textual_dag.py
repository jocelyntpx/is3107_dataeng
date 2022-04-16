from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator
)

import sys
sys.path.append('/home/airflow/airflow/scripts')
import stocknews_call
import reddit_call
import concat_textual_data
import sentiment_analysis
import bigquery_call


default_args = {
    'owner': 'adminjw',
    'depends_pn_past': False,
    'email': ['123@jun.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}


# PROJECT_ID = "united-planet-344907"
PROJECT_ID = "is3107-stocks-project"
DATASET_NAME = "sentiment"
CONN_ID =  "bq_conn"
POSTGRES_CONN_ID = "postgres_user"
TABLE_1 = "combined_sentiment"
LOCATION = "asia-southeast1"
SCHEMA_1 = [
        {"name": "_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "datetime_created", "type": "DATETIME", "mode": "NULLABLE"},
        {"name": "source", "type": "STRING", "mode": "NULLABLE"},
        {"name": "ticker", "type": "STRING", "mode": "REPEATED"},
        {"name": "publisher", "type": "STRING", "mode": "NULLABLE"},
        {"name": "text", "type": "STRING", "mode": "NULLABLE"},
        {"name": "title", "type": "STRING", "mode": "NULLABLE"},
        {"name": "score", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "url", "type": "STRING", "mode": "NULLABLE"},
        {"name": "probability", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "sentiment", "type": "STRING", "mode": "NULLABLE"},
    ]


# [START instantiate_dag]
with DAG(
    'retrieve_daily_textual_data',
    default_args=default_args,
    description='retrieve daily stock news and reddit threads data',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['retrieve'],
) as dag:
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this

    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create-dataset",
        dataset_id=DATASET_NAME,
        location=LOCATION)

    create_table = BigQueryCreateEmptyTableOperator(
        task_id="create_table",
        dataset_id=DATASET_NAME,
        table_id=TABLE_1,
        schema_fields=SCHEMA_1,
        location=LOCATION)

    retrieve_stocknews_task = PythonOperator(
        task_id = 'daily_stock_news',
        python_callable = stocknews_call.get_stocknews_data)

    retrieve_reddit_task = PythonOperator(
        task_id = 'daily_reddit_threads',
        python_callable = reddit_call.get_reddit_data)

    get_sentiment_twitter = PythonOperator(
        task_id = 'get_twitter_sentiment_analysis',
        python_callable = sentiment_analysis.twitter_sentiment)

    get_sentiment_stocknews = PythonOperator(
        task_id = 'get_stocknews_sentiment_analysis',
        python_callable = sentiment_analysis.stocknews_sentiment)

    get_sentiment_reddit = PythonOperator(
        task_id = 'get_reddit_sentiment_analysis',
        python_callable = sentiment_analysis.reddit_sentiment)

    combine_textual_task = PythonOperator(
        task_id = 'combine_textual_data',
        python_callable = concat_textual_data.combine_textual_db)

    upload_mongodb_data_bigquery = PythonOperator(
        task_id = 'upload_mongodb_data_to_bq',
        python_callable = bigquery_call.Mongo_To_BigQueryTable,
        op_kwargs = {'PARTS': 2})

    upload_mongodb_data_gcs = PythonOperator(
        task_id = 'upload_mongodb_data_to_gcs',
        python_callable = bigquery_call.Mongo_TO_GCS) 

    finish_pipeline = DummyOperator(
    task_id = 'finish_pipeline')   
    # [END documentation]



create_dataset >> create_table >> (retrieve_reddit_task, retrieve_stocknews_task, get_sentiment_twitter) 
retrieve_reddit_task >> get_sentiment_reddit
retrieve_stocknews_task >> get_sentiment_stocknews
get_sentiment_twitter 
(get_sentiment_reddit, get_sentiment_stocknews, get_sentiment_twitter) >> combine_textual_task >> (upload_mongodb_data_bigquery, upload_mongodb_data_gcs) >> finish_pipeline
