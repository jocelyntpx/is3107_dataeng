from datetime import datetime, timedelta
from re import L
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import sys
# from sentiment_analysis import get_sentiment
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

    upload_mongodb_data = PythonOperator(
        task_id = 'upload_mongodb_data_to_bq',
        python_callable = bigquery_call.Mongo_To_BigQueryTable)
    # [END documentation]

retrieve_reddit_task >> get_sentiment_reddit
retrieve_stocknews_task >> get_sentiment_stocknews
get_sentiment_twitter 
(get_sentiment_reddit, get_sentiment_stocknews, get_sentiment_twitter) >> combine_textual_task >> upload_mongodb_data
