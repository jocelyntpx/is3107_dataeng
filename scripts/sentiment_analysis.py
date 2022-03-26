import flair
import pymongo
import pandas as pd
import re
import json
import numpy as np

def get_sentiment():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mydb.list_collection_names()

    # create another collection
    combined_text_cleaned = mydb["combined_text_cleaned"]

    df = pd.json_normalize(list(mydb.combined_text_data.find()))

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
    combined_text_cleaned.insert_many(data)
