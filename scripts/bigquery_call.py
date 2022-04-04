
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pymongo
from bson.json_util import dumps, loads
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

projectId ='united-planet-344907'
datasetId = 'combined_test_cleaned'
tableId ='combined_test_cleaned_table'

def Mongo_To_BigQueryTable():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["combined_sentiment_data"]
    collection = mycol.find()
    list_cur = list(collection)
    bq_hook = BigQueryHook()
    bq_hook.insert_all(project_id=projectId, dataset_id=datasetId, table_id=tableId, rows = list_cur)


