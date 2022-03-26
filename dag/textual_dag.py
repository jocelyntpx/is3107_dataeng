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

default_args = {
    'owner': 'adminjw',
    'depends_pn_past': False,
    'email': ['123@jun.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016,1,1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
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
    retrieve_stock_news_task = PythonOperator(
        task_id = 'daily_stock_news',
        python_callable = stocknews_call.get_stocknews_data)

    retrieve_reddit_task = PythonOperator(
        task_id = 'daily_reddit_threads',
        python_callable = reddit_call.get_reddit_data)

    retrieve_tweet_task = BashOperator(
        task_id = 'daily_tweets',
        bash_command = 'python /home/airflow/airflow/scripts/tweetpy_call.py')

    combine_textual_task = PythonOperator(
        task_id = 'combine_textual_data',
        python_callable = concat_textual_data.combine_textual_db)

    get_sentiment_task = PythonOperator(
        task_id = 'get_sentiment_analysis',
        python_callable = sentiment_analysis.get_sentiment)
    # [END documentation]

(retrieve_stock_news_task, retrieve_reddit_task) >> combine_textual_task >> get_sentiment_task
retrieve_tweet_task
