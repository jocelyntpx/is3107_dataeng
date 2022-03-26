import pymongo
import json
import pandas as pd
from datetime import timedelta, datetime

def combine_textual_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]

    combined_text_data = mydb["combined_text_data"]
    combined_text_data.drop()
    combined_text_data = mydb["combined_text_data"]

    df = pd.json_normalize(list(mydb.twitter.find()))
    # df = df[df['datetime_created'] == (datetime.today() - timedelta(days=1)).date()]
    arr_twitter = df.to_json(orient='records', lines=True, default_handler=str).split('\n')[:-1]

    arr_twitter = [json.loads(x) for x in arr_twitter]
    combined_text_data.insert_many(arr_twitter)

    arr_stocknews = list(mydb['stocknews'].find())
    combined_text_data.insert_many(arr_stocknews)

    arr_reddit = list(mydb['reddit'].find())
    combined_text_data.insert_many(arr_reddit)
