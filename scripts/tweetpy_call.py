import pymongo
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from datetime import datetime
from dateutil import tz
import sys
import smtplib, ssl
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/airflow/airflow/keys/bq_key.json'

# requested to get credentials at http://apps.twitter.com
consumer_key    = 'cK3DmGlD6d4PMRB59MmUDpqHc'
consumer_secret = 'KhoQQ94lyVHa5LI3VYjk58JRaS52aecgP1kTS2K7ceUm4NWnSi'
access_token    = '1141341991-OE5Qf5ck245amYIjxRtrRCLjtsq8l6cOc4iHiig'
access_secret   = '6xq1Oed2aqLuJ4vPRUWfuHfbhAzZrptlfk4UVExECuEgz'

#email for disconnected stream
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "nusmerch@gmail.com"  # Enter your address
receiver_email = "nusmerch@gmail.com"  # Enter receiver address
password = input("Type your password and press enter: ")
message = """\
Subject: Twitter stream disconnected

Twitter stream has disconnected. Please reconnect."""

tickers_dict={
    'singapore airlines': 'Singapore Airlines Limited',
    'dbs': 'DBS Group Holdings Ltd',
    'comfortdelgro': 'ComfortDelGro Corporation Limited',
    'genting': 'Genting Singapore Limited',
    'capitaland': 'CapitaLand Integrated Commercial Trust',
    'uob': 'United Overseas Bank Limited',
    'mapletree logistics': 'Mapletree Logistics Trust',
    'mapletree commercial': 'Mapletree Commercial Trust',
    'sats': 'SATS Ltd',
    'wilmar': 'Wilmar International Limited',
    'singtel': 'Singapore Telecommunications Limited',
    'city dev': 'City Developments Limited',
    'yangzijiang shipbuilding': 'Yangzijiang Shipbuilding (Holdings) Ltd',
    'thai beverage public company': 'Thai Beverage Public Company Limited',
    'venture corporation': 'Venture Corporation Limited',
    'sembcorp': 'Sembcorp Industries Ltd',
    'ascendas': 'Ascendas Real Estate Investment Trust',
    'frasers': 'Frasers Logistics & Commercial Trust',
    'hongkong land holdings': 'Hongkong Land Holdings Limited',
    'st engineering': 'Singapore Technologies Engineering Ltd'
}

class TweetsListener(StreamListener):
    def __init__(self, *args, **kwargs):
        self.bq_table=kwargs['table']
        kwargs.pop('table',None)
        super(TweetsListener, self).__init__(*args, **kwargs)
        self.count=0
        
    
    def on_data(self, data):
        #####################################
        if self.count >= 5: 
            sys.exit("Reached 5 tweets") #as Twitter is streaming, our group will use a counter to stop it to manage the data.
                                            #else, it is supposed to continuosly stream.
         #####################################
            
        try:
            tweet_data = json.loads(data)

            if 'RT @' not in tweet_data['text']:
            
                try:
                    full_tweet = tweet_data['extended_tweet']['full_text']
                except Exception as e:
                    full_tweet = tweet_data['text']
            
                ticker_list = []
                for ticker, name in tickers_dict.items():
                    if ticker in full_tweet.lower():
                        ticker_list.append(name)
                # if ("singapore airlines" in (full_tweet.lower())):
                #     ticker_list.append("Singapore Airlines Limited")
                # if ("dbs" in (full_tweet.lower())):
                #     ticker_list.append("DBS Group Holdings Ltd")
                # if ("comfortdelgro" in (full_tweet.lower())):
                #     ticker_list.append("ComfortDelGro Corporation Limited")
                # if ("genting" in (full_tweet.lower())):
                #     ticker_list.append("Genting Singapore Limited")
                # if ("capitaland" in (full_tweet.lower())):
                #     ticker_list.append("CapitaLand Integrated Commercial Trust")
                # if ("uob" in (full_tweet.lower())):
                #     ticker_list.append("United Overseas Bank Limited")
                # if ("mapletree logistics" in (full_tweet.lower())):
                #     ticker_list.append("Mapletree Logistics Trust")
                # if ("mapletree commercial" in (full_tweet.lower())):
                #     ticker_list.append("Mapletree Commercial Trust")
                # if ("sats" in (full_tweet.lower())):
                #     ticker_list.append("SATS Ltd")
                # if ("wilmar" in (full_tweet.lower())):
                #     ticker_list.append("Wilmar International Limited")
                # if ("singtel" in (full_tweet.lower())):
                #     ticker_list.append("Singapore Telecommunications Limited")
                # if ("city dev" in (full_tweet.lower())):
                #     ticker_list.append("City Developments Limited")
                # if ("yangzijiang shipbuilding" in (full_tweet.lower())):
                #     ticker_list.append("Yangzijiang Shipbuilding (Holdings) Ltd")
                # if ("thai beverage public company" in (full_tweet.lower())):
                #     ticker_list.append("Thai Beverage Public Company Limited")
                # if ("venture corporation" in (full_tweet.lower())):
                #     ticker_list.append("Venture Corporation Limited")
                # if ("sembcorp" in (full_tweet.lower())):
                #     ticker_list.append("Sembcorp Industries Ltd")
                # if ("ascendas" in (full_tweet.lower())):
                #     ticker_list.append("Ascendas Real Estate Investment Trust")
                # if ("frasers" in (full_tweet.lower())):
                #     ticker_list.append("Frasers Logistics & Commercial Trust")
                # if ("hongkong land holdings" in (full_tweet.lower())):
                #     ticker_list.append("Hongkong Land Holdings Limited")
                # if ("st engineering" in (full_tweet.lower())):
                #     ticker_list.append("Singapore Technologies Engineering Ltd")
                
                # convert UTC to GMT+8
                dtime = tweet_data['created_at']
                new_datetime = datetime.strftime(datetime.strptime(dtime,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
                from_zone = tz.gettz('UTC')
                to_zone = tz.gettz('Singapore')
                utc = datetime.strptime(new_datetime, '%Y-%m-%d %H:%M:%S')
                utc = utc.replace(tzinfo=from_zone)
                local = utc.astimezone(to_zone)
                local_dt = local.strftime('%Y-%m-%d %H:%M:%S')
                
                tweet_data_filtered = {
                    "data": [
                        {
                            "datetime_created": local_dt,
                            "source": "Twitter",
                            "ticker": ticker_list,
                            "publisher": tweet_data['user']['screen_name'],
                            "text": full_tweet

                        }
                    ]
                }

                self.count += 1

                # if tweet_data['user']['screen_name'] in ['test92806851']: #test account
                if tweet_data['user']['screen_name'] in ['LawrenceWongST','OCBCBank','ChannelNewsAsia','govsingapore',
                    'TODAYonline','MFAsg','dbsbank','leehsienloong','MAS_sg','straits_times','YahooSG','chuanjin1','SGX']:
                    to_insert_bq = {
                        "data": [
                            {
                                "datetime_created": local_dt,
                                "twitter_username": tweet_data['user']['screen_name'],
                                "tweet": full_tweet

                            }
                        ]
                    }
                    row_to_insert = to_insert_bq["data"]
                    errors = bigquery_client.insert_rows_json(self.bq_table, row_to_insert)
                    if errors != []:
                        print("error inserting into big query")
                        print(errors)
                    print(to_insert_bq["data"][0])

                if ticker_list != []:
                    tweet_db.insert_one(tweet_data_filtered["data"][0])
                    print(tweet_data_filtered["data"][0])
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True
  
    def on_error(self, status_code):
        if status_code == 420:
            #send email when on_data disconnects the stream
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            #returning False in on_data disconnects the stream
            return False


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["is3107db"]
tweet_db = mydb["twitter"]

# big query
bigquery_client = bigquery.Client()
dataset_ref = bigquery_client.dataset('twitter')  # get BQ dataset
table_ref = dataset_ref.table('real_time_tweets')  # get BQ table
table = bigquery_client.get_table(table_ref)  # API call

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
twitter_stream = Stream(auth, TweetsListener(table=table))
twitter_stream.filter(
    track=list(tickers_dict.values()),
    # follow=['1507756052405653511'], #test account
    follow=['282161299','66793353','38400130','56883209','41085467','77165249','95310018','34568673','85774665','37874853','115624161','29213315','2362057826'],
    languages=['en']
) #we are interested in tweets with these stocks and tweets from these twitter accounts
