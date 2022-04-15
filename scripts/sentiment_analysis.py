import flair
import pymongo
import pandas as pd
import re
import json
import numpy as np
from datetime import datetime

def get_sentiment(table):
    if table.count_documents({}) == 0:
        raise ValueError('Database is empty')
    df = pd.json_normalize(list(table.find()))

    def clean(s):
        user = re.compile(r"(?i)@[a-z0-9_]+|#[a-z0-9_]+")
        whitespace = re.compile(r"\s+")
        web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")

        # remove emojis
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)

        # we then use the sub method to replace anything matching
        s = user.sub('', s)
        s = whitespace.sub(' ', s)
        s = web_address.sub('', s)
        s = emoji_pattern.sub('', s)

        return s

    sentiment_model = flair.models.TextClassifier.load('en-sentiment')

    # we will append probability and sentiment preds later
    probs = []
    sentiments = []

    # use regex expressions (in clean function) to clean tweets
    df['text'] = [clean(s) if not pd.isna(s) else '' for s in df['text']]

    for s in df['text'].to_list():
        if not pd.isna(s):
        # make prediction
            sentence = flair.data.Sentence(s)
            sentiment_model.predict(sentence)
            # extract sentiment prediction
            probs.append(sentence.labels[0].score)  # numerical score 0-1
            sentiments.append(sentence.labels[0].value)  # 'POSITIVE' or 'NEGATIVE'
        else:
            probs = np.nan
            sentiments = np.nan

    # add probability and sentiment predictions to tweets dataframe
    df['probability'] = probs
    df['sentiment'] = sentiments

    data = df.to_json(orient='records', lines=True, default_handler=str).split('\n')[:-1]
    data = [json.loads(x) for x in data]
    # combined_text_cleaned.insert_many(data)
    return data

def stocknews_sentiment():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["stocknews"]
    data = get_sentiment(mycol)
    mycol.delete_many({})
    mycol.insert_many(data)

def twitter_sentiment():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["twitter"]

    df = pd.json_normalize(list(mycol.find()))
    # Filtering for 1 day's of tweets
    # df = df[df['datetime_created'] == (datetime.today() - timedelta(days=1)).date()]
    arr_twitter = df.to_json(orient='records', lines=True, default_handler=str).split('\n')[:-1]
    arr_twitter = [json.loads(x) for x in arr_twitter]

    twitter_sentiment = mydb["twitter_sentiment"]
    if twitter_sentiment.count_documents({}) != 0:
        # If database has previous day's data, clear it
        twitter_sentiment.delete_many({})

    twitter_sentiment.insert_many(arr_twitter)

    # remove the data that is posted earlier than today
    mydb.twitter.delete_many(
        { 'datetime_created': {'$lte': str(datetime.today().date())}}
    )

    data = get_sentiment(twitter_sentiment)
    twitter_sentiment.delete_many({})
    twitter_sentiment.insert_many(data)

def reddit_sentiment():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["reddit"]
    data = get_sentiment(mycol)
    mycol.delete_many({})
    mycol.insert_many(data)
