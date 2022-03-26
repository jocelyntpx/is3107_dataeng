import pymongo
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from datetime import datetime
from dateutil import tz
import sys

# requested to get credentials at http://apps.twitter.com
consumer_key    = 'cK3DmGlD6d4PMRB59MmUDpqHc'
consumer_secret = 'KhoQQ94lyVHa5LI3VYjk58JRaS52aecgP1kTS2K7ceUm4NWnSi'
access_token    = '1141341991-OE5Qf5ck245amYIjxRtrRCLjtsq8l6cOc4iHiig'
access_secret   = '6xq1Oed2aqLuJ4vPRUWfuHfbhAzZrptlfk4UVExECuEgz'

    
class TweetsListener(StreamListener):
    def __init__(self, *args, **kwargs):
        super(TweetsListener, self).__init__(*args, **kwargs)
        self.count=0
        
    
    def on_data(self, data):
        if self.count > 5: 
            sys.exit("Reached 5 tweets") #as Twitter is streaming, our group will use a counter to stop it to manage the data.
                                            #else, we intend to let it stream.
            
        try:
            tweet_data = json.loads( data )
            
            ticker_list = []   #to edit after we decide on the list of tickers
            if ("stocks" in (tweet_data['text'].lower())):
                ticker_list.append("stocks")
            if ("SIA" in (tweet_data['text'].lower())):
                ticker_list.append("SIA")
                
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
                        "text": tweet_data['text'],
                        "score": tweet_data['favorite_count']

                    }
                ]
            }

            self.count += 1
            mycol.insert_one(tweet_data_filtered["data"][0])
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True
  
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["is3107db"]
mycol = mydb["twitter"]
# mycol.drop()
# mycol = mydb["twitter"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
twitter_stream = Stream(auth, TweetsListener())
twitter_stream.filter(
    track=['SPH', 'SIA', 'OCBC', 'DBS', 'POSB', 'Singtel', 'ComfortDelGro', 'UOB', 'Sembcorp', 'Keppel', 'Mapletree'], 
    locations=(103.6920359,1.1304753,104.0120359,1.4504753)
) #we are interested in tweets with these stocks and are from Singapore
