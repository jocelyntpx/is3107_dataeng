
from dataclasses import dataclass
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
import pymongo
from bson.json_util import dumps, loads
from datetime import datetime, timedelta
from google.cloud import bigquery

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

projectId ='united-planet-344907'
datasetId = 'combined_sentiment'
tableId ='combined_sentiment_table'

GOOGLE_CONN_ID = "google_cloud_default"    
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")
BUCKET_NAME ='is3107-stock-analysis'
GS_PATH = 'data/textual_data/'


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["is3107db"]
mycol = mydb["combined_sentiment_data"]
collection = mycol.find(
                {'datetime_created': {
                    '$gte': str((datetime.today()-timedelta(days=1)).date()),
                    '$lt': str(datetime.today().date())
                    }
                })
list_cur = list(collection)

def Mongo_TO_GCS():

    gcs_hook = GoogleCloudStorageHook(GOOGLE_CONN_ID)
    # turn list into json 
    json_data = dumps(list_cur, indent = 2) 
    # Writing data to file textual_data_{date}.json
    file_name = 'textual_data_'+INSERT_DATE+'.json' 
    with open(file_name, 'w') as file:
        file.write(json_data)
    gcs_hook.upload(BUCKET_NAME, GS_PATH +file_name, file_name)    


def Mongo_To_BigQueryTable():
    bq_hook = BigQueryHook()

    # check if yesterday's data has been inputteds
    query = """
        SELECT *
        FROM `united-planet-344907.combined_test_cleaned.combined_test_cleaned_table` AS t 
        WHERE t.datetime_created BETWEEN DATE_SUB(CURRENT_DATE('''GMT'''), INTERVAL 1 DAY) AND current_date('''GMT''');
    """
    bq_client = bigquery.Client(project = bq_hook._get_field(projectId), credentials = bq_hook._get_credentials())
    data = bq_client.query(query).result()

    # if yesterday's data isn't found, add inside bigquery
    if data.total_rows == 0:

        # TODO: only add in yesterday's informaiton, not all (appending method)
        bq_hook.insert_all(project_id=projectId, dataset_id=datasetId, table_id=tableId, rows = list_cur)






