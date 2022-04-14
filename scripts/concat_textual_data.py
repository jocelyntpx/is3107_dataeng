import pymongo

def combine_textual_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["textual_db"]

    combined_text_data = mydb["combined_sentiment_data"]

    arr_twitter = list(mydb['twitter_sentiment'].find())
    combined_text_data.insert_many(arr_twitter)

    arr_stocknews = list(mydb['stocknews'].find())
    combined_text_data.insert_many(arr_stocknews)

    arr_reddit = list(mydb['reddit'].find())
    combined_text_data.insert_many(arr_reddit)
    