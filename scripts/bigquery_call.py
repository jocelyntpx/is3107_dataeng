
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pymongo
from bson.json_util import dumps, loads


'''
Using reddit database
'''
def Mongo_To_GCS2():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["reddit"]
    collection = mycol.find()
    # Converting cursor to the list of dictionaries
    list_cur = list(collection)
    # print(list_cur)

    # Converting to the JSON
    json_data = dumps(list_cur) 

    BQ_hook(json_data)



def BQ_hook(jsonData): 
    projectId ='united-planet-344907'
    datasetId='reddit'
    tableId = 'reddit_table'

    # CANNOT READ THE VALUES INSIDE, can add but returns null 
    # Testing it with dummy data first 
    rows=[
        {'json': {
            'text':'textaa',
            'test':'testaa'
            }
        }, 
        {'json': {
            'text':'texta',
            'test':'testa'
            }
        }]
    
    bq_hook = BigQueryHook()
    bq_hook.insert_all(project_id=projectId, dataset_id=datasetId, table_id=tableId, rows = rows, ignore_unknown_values = True)
