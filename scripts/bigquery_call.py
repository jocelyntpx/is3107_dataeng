
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
datasetId = 'sentiment'
tableId ='combined_sentiment'

GOOGLE_CONN_ID = "google_cloud_default"    
INSERT_DATE = datetime.now().strftime("%Y-%m-%d")
BUCKET_NAME ='is3107-stock-analysis'
GS_PATH = 'data/textual_data/'


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["textual_db"]
mycol = mydb["combined_sentiment_data"]

# double check that we are retrieving one day's worth of data.
collection = mycol.find(
                {'datetime_created': {
                    '$gte': str((datetime.today()-timedelta(days=1)).date()),
                    '$lt': str(datetime.today().date())
                    }
                })
list_cur = list(collection)

def chunk(l,n):
  d,r = divmod(len(l),n) 
  for i in range (n):
    si= (d+1)* (i if i<r else r) + d*(0 if i < r else i-r)
    yield l[si:si+(d+1 if i < r else d)]
    
def Mongo_TO_GCS():

    gcs_hook = GoogleCloudStorageHook(GOOGLE_CONN_ID)
    # turn list into json 
    json_data = dumps(list_cur, indent = 2) 
    # Writing data to file textual_data_{date}.json
    file_name = 'textual_data_'+INSERT_DATE+'.json' 
    with open(file_name, 'w') as file:
        file.write(json_data)
    gcs_hook.upload(BUCKET_NAME, GS_PATH +file_name, file_name)    

def Mongo_To_BigQueryTable(PARTS):
    bq_hook = BigQueryHook()

    # delete any rows from BQ with yesterday's data
    query = """
        DELETE FROM `united-planet-344907.sentiment.combined_sentiment` AS t
        WHERE t.datetime_created BETWEEN DATE_SUB(CURRENT_DATE('''GMT'''), INTERVAL 1 DAY) AND current_date('''GMT''')
        AND t.datetime_created < TIMESTAMP_SUB(t.datetime_created, INTERVAL 30 MINUTE);
    """
    bq_client = bigquery.Client(project = bq_hook._get_field(projectId), credentials = bq_hook._get_credentials())
    data = bq_client.query(query).result()
    print(data)
    lst = list(chunk(data, PARTS))
    for res in lst:
        bq_hook = BigQueryHook()
        bq_hook.insert_all(project_id=projectId, dataset_id=datasetId, table_id=tableId, rows = res)
