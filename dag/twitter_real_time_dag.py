from datetime import datetime, timedelta
from re import L
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# import sys
# # from sentiment_analysis import get_sentiment
# sys.path.append('/home/airflow/airflow/scripts')
# import stocknews_call
# import reddit_call
# import concat_textual_data
# import sentiment_analysis

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
    'real_time_tweet_streaming',
    default_args=default_args,
    description='stream tweets in realtime',
    schedule_interval="0 * * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['retrieve'],
) as dag:
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this

    retrieve_tweet_task = BashOperator(
        task_id = 'daily_tweets',
        bash_command = 'python /home/airflow/airflow/scripts/tweetpy_call.py')
    # [END documentation]
