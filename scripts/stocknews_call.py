import pymongo
import vanity
import pandas as pd
import json
from datetime import datetime, timedelta

def get_stocknews_data():
    tickers = ['DBSDY','UOVEY','SINGY','SE','FXSG','EWS','MTGCF','STX','FUTU','ACDSF']
    ticker_names = ['DBS Group Holdings Ltd','United Overseas Bank Limited','Singapore Airlines Limited','Sea Limited','Invesco CurrencyShares Singapore Dollar',
    'iShares MSCI Singapore Capped ETF','Mapletree North Asia Commercial Trust','Seagate Technology plc','Futu Holdings Limited','Ascendas Real Estate Investment Trust']

    doc = vanity.get_jsonparsed_data("https://stocknewsapi.com/api/v1?tickers=DBSDY,UOVEY,SINGY,SE,FXSG,EWS,MTGCF,STX,FUTU&items=50&token=cdxgrhebia7lvobqdvhfbhhk0wahvwlyo2e9kkmj")['data']

    df = pd.json_normalize(doc)
    df['datetime_created'] = [pd.to_datetime(x).tz_convert('Asia/Singapore').strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(x) else pd.NaT for x in df['date']]

    df['date'] = [pd.to_datetime(x) if not pd.isna(x) else pd.NaT for x in df['datetime_created']]
    df = df[df['date'] == (datetime.today() - timedelta(days=1)).date()]
    df.rename(columns={'source_name':'publisher','news_url':'url','tickers':'ticker'}, inplace=True)
    df['source'] = 'stocknews'
    df['ticker'] = [[ticker_names[tickers.index(x)] for x in lst if x in tickers] for lst in df['ticker']]
    df.drop(columns=['image_url','topics','type','date','sentiment'], inplace=True)

    data = df.to_json(orient='records', lines=True).split('\n')[:-1]
    data = [json.loads(x) for x in data]

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["stocknews"]

    if mycol.count_documents({}) != 0:
        # If database has other day's data, clear it
        mycol.delete_many({})

    mycol.insert_many(data)
