from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta  
import datetime as dt
from dateutil import tz
import praw
import pymongo
import time

USERNAME = 'Still_Statistician32'
PASSticker = 'BD99cjOO'
CLIENT_ID = 'CSwmabTf7mzgHTmg2zynPg'
SECRET_TOKEN = '9VSTmChi6sqT5JCct1ha8Y3ctxKeVg'

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

def get_reddit_data():
    # reddit = praw.Reddit(client_id=CLIENT_ID, 
    #                  client_secret=SECRET_TOKEN,
    #                  passticker=PASSticker, 
    #                  user_agent='TESTING praw accessAPI:v0.0.1 (by /u/Still_Statistician32)',
    #                  username=USERNAME)
    # subreddit = reddit.subreddit('singapore')
    # sgx_list = []
    # start = time.time()
    # for word in tickers_dict.keys():
    #     sgx_subreddit = subreddit.search(word)
    #     from_zone = tz.gettz('UTC')
    #     to_zone = tz.gettz('Singapore')
    #     for posts in sgx_subreddit:
    #         sgx_dict = {}
    #         # Convert UTC to GMT+8
    #         new_datetime = str(dt.datetime.fromtimestamp(posts.created))
    #         utc = datetime.strptime(new_datetime, '%Y-%m-%d %H:%M:%S')
    #         utc = utc.replace(tzinfo=from_zone)
    #         local = utc.astimezone(to_zone)
    #         local_dt = local.strftime('%Y-%m-%d %H:%M:%S')
            
    #         if (local_dt == (datetime.today() - timedelta(days=1)).date()):
    #             sgx_dict['datetime_created'] = local_dt
    #             sgx_dict['source'] = 'Reddit'
    #             ticker_list = []
    #             for ticker, name in tickers_dict.items():
    #                 if (ticker in posts.selftext.lower()) or (ticker in posts.title.lower()):
    #                     ticker_list.append(name)
    #             sgx_dict['ticker'] = ticker_list
    #             sgx_dict['publisher'] = str(posts.author)
    #             sgx_dict['text'] = posts.selftext
    #             sgx_dict['title'] = posts.title
    #             sgx_dict['score'] = posts.score
    #             sgx_dict['url'] = posts.url
    #             sgx_list.append(sgx_dict)
    # end = time.time()
    # print('Time execution duration (secs): ', end-start)
    # print(sgx_list)
    
    sgx_list = [
        {'datetime_created': '2022-02-14 07:49:34', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'skyscraper56', 'text': '', 'title': 'Passengers can look forward to new cabin features when Singapore Airlines takes delivery of new fleet', 'score': 39, 'url': 'https://str.sg/wW6w'}, {'datetime_created': '2022-03-20 06:06:32', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'AsgardianGoat', 'text': "I called Singapore Airlines US number and I was on hold for 4 hours and 30 minutes, I finally hung up. I then tried their online chat service, which after waiting for about an hour disconnected me, not once, but twice, saying that agents are not available. There is no way I can reach these guys. I am afraid to purchase a ticket from them because if I need to make a change I won't be able to change the ticket. I know they have online self service, but not everything can be done online.", 'title': 'Singapore Airlines Customer Service Hold Times', 'score': 9, 'url': 'https://www.reddit.com/r/singapore/comments/ti65fp/singapore_airlines_customer_service_hold_times/'}, {'datetime_created': '2022-02-24 18:35:51', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'MicrotechAnalysis', 'text': '', 'title': 'Singapore Airlines posts first quarterly profit since start of pandemic', 'score': 87, 'url': 'https://www.todayonline.com/world/singapore-airlines-posts-first-quarterly-profit-start-pandemic-1825941'}, {'datetime_created': '2022-02-01 07:03:36', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'PhebeSandifer', 'text': '', 'title': 'Singapore Airlines To Start Operating Daily Flights to Bali on February 16', 'score': 198, 'url': 'https://www.travelinglifestyle.net/singapore-airlines-to-start-operating-daily-flights-to-bali-on-february-16/'}, {'datetime_created': '2021-12-08 09:46:10', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'misty1497', 'text': '', 'title': 'Has anyone been able to get ahold of Singapore Airlines? I’ve been on hold for a ridiculous amount of time and don’t know if I’ll ever speak to someone.', 'score': 458, 'url': 'https://i.redd.it/7r7a0yuq48481.jpg'}, {'datetime_created': '2022-02-03 12:41:02', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'MicrotechAnalysis', 'text': '', 'title': "Singapore Airlines ranked top global airline, leading Asian firm in Fortune's top 50 list", 'score': 47, 'url': 'https://www.straitstimes.com/singapore/transport/singapore-airlines-ranked-top-global-airline-leading-asian-firm-in-fortunes-top-50-list'}, {'datetime_created': '2021-12-02 14:32:34', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'P838', 'text': '', 'title': 'The wait time at Singapore Airlines customer service office @ ION Orchard ~ 4 hour wait', 'score': 242, 'url': 'https://i.redd.it/o63tl6qeq2381.jpg'}, {'datetime_created': '2022-01-13 15:07:54', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'MicrotechAnalysis', 'text': '', 'title': 'Singapore Airlines raises US$600 million in US dollar bond deal', 'score': 32, 'url': 'https://www.todayonline.com/world/singapore-airlines-raises-us600-million-us-dollar-bond-deal-1789691'}, {'datetime_created': '2021-11-20 23:50:33', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'MicrotechAnalysis', 'text': '', 'title': 'Singapore Airlines unveiled a swanky new lie-flat business class seat on its Boeing 737 MAX plane', 'score': 58, 'url': 'https://www.businessinsider.com/photos-new-singapore-airlines-narrowbody-lie-flat-business-class-seat-2021-11'}, {'datetime_created': '2021-11-05 14:05:55', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'MyWholeTeamsDead', 'text': '', 'title': 'Singapore Airlines SFO-SIN flight cancelled after plane makes contact with another aircraft on the ground', 'score': 79, 'url': 'https://www.channelnewsasia.com/singapore/singapore-airlines-san-francisco-flight-cancelled-sq33-2293231'}, {'datetime_created': '2021-10-05 10:13:52', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'haikallp', 'text': '', 'title': 'Two Singapore Airlines A380s towed along public road to be scrapped at Changi Exhibition Centre', 'score': 126, 'url': 'https://www.channelnewsasia.com/singapore/sia-a380-scrap-singapore-airlines-changi-2215261'}, {'datetime_created': '2021-11-12 13:55:27', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'annoyedwityou', 'text': '', 'title': 'Singapore Airlines has 79% of fleet ready to use on any demand increase', 'score': 37, 'url': 'https://sg.finance.yahoo.com/news/singapore-airlines-79-fleet-ready-032419078.html'}, {'datetime_created': '2021-10-11 21:35:47', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'Angryangmo', 'text': '', 'title': 'Singapore Airlines launches seasonal flights to Vancouver, first to Canada since 2009', 'score': 62, 'url': 'https://www.channelnewsasia.com/business/singapore-airlines-vancouver-canada-flight-service-vtl-covid-19-vaccinated-travel-lane-2236071'}, {'datetime_created': '2021-10-02 09:31:50', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'MyWholeTeamsDead', 'text': '', 'title': 'This dog flew Singapore Airlines business class from Sydney to Italy', 'score': 215, 'url': 'https://www.executivetraveller.com/news/this-dog-flew-singapore-airlines-business-class-from-sydney-to-italy'}, {'datetime_created': '2021-09-16 20:16:26', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'Tiger2021J', 'text': '', 'title': 'Singapore Airlines uses up last S$600 million of 2020 rights issue', 'score': 113, 'url': 'https://www.businesstimes.com.sg/transport/singapore-airlines-uses-up-last-s600-million-of-2020-rights-issue'}, {'datetime_created': '2021-12-04 21:03:51', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'PrataKosong-', 'text': '', 'title': 'The Singapore Airlines 2021 Experience - What’s Changed Onboard?', 'score': 0, 'url': 'https://youtu.be/Kav6n7tTCQY'}, {'datetime_created': '2021-07-08 18:01:54', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'stforumtroll2', 'text': '', 'title': 'Cash-rich Singapore Airlines aims for regional dominance as rivals pull back', 'score': 120, 'url': 'https://www.todayonline.com/singapore/cash-rich-singapore-airlines-aims-regional-dominance-rivals-pull-back?cid=tdy%20tg_tg-pm_social-msging-free_09102018_today'}, {'datetime_created': '2021-08-04 19:52:12', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'pyonguno', 'text': '', 'title': 'Singapore Airlines A380 kicks up desert dust as it departs Australian storage facility', 'score': 149, 'url': 'https://www.traveller.com.au/singapore-airlines-a380-kicks-up-desert-dust-as-it-departs-australian-storage-facility-h1xmvs'}, {'datetime_created': '2021-09-07 21:16:16', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'Doraemonhacker', 'text': '', 'title': 'Review: COVID-era service on Singapore Airlines A350-900 Business Class, Singapore to Munich.', 'score': 26, 'url': 'https://milelion.com/2021/09/07/review-covid-era-service-on-singapore-airlines-a350-900-business-class-singapore-to-munich/?utm_source=telegram&utm_medium=telegram&utm_campaign=roars'}, {'datetime_created': '2021-05-25 15:58:16', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'vaish7848', 'text': '', 'title': 'Singapore Airlines reroutes flights to avoid Belarus airspace after forced landing of Ryanair plane', 'score': 193, 'url': 'https://www.channelnewsasia.com/news/singapore/singapore-airlines-belarus-airspace-flights-roman-protasevich-14881388'}, {'datetime_created': '2021-08-13 18:00:19', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'theloneranger_55', 'text': '', 'title': "Singapore Airlines ends MVC salary cuts for S'pore-based staff from Aug 1", 'score': 11, 'url': 'https://www.straitstimes.com/business/companies-markets/singapore-airlines-ends-mvc-salary-cuts-for-singapore-based-staff-from'}, {'datetime_created': '2021-05-31 06:22:54', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'JiPaiHongGanLiao', 'text': '', 'title': 'Singapore airlines updated their marketing Batik Motif, the first time since 1974. Uniforms will not be updated. (This is what you see on their cardholders, Duty free SQ stuff etc)', 'score': 257, 'url': 'https://www.reddit.com/gallery/nom5ef'}, {'datetime_created': '2021-04-28 09:17:11', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'Varantain', 'text': '', 'title': 'Singapore Airlines adding new award category - is a KrisFlyer devaluation coming?', 'score': 84, 'url': 'https://mainlymiles.com/2021/04/28/singapore-airlines-adding-new-award-category-is-a-krisflyer-devaluation-coming/'}, {'datetime_created': '2021-10-22 23:09:44', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'Happyboynumber1', 'text': '', 'title': 'Welcome Back Singapore Airlines!', 'score': 0, 'url': 'https://www.youtube.com/watch?v=_w6R_jwfTAQ'}, {'datetime_created': '2021-06-20 16:31:58', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'BabaDuda', 'text': '', 'title': 'The Runway Was Not Clear (Singapore Airlines Flight 006/SQ006)', 'score': 27, 'url': 'https://www.youtube.com/watch?v=8rXmskgv8nw'}, {'datetime_created': '2021-03-26 10:32:23', 'source': 'Reddit', 'ticker': ['Singapore Airlines Limited'], 'publisher': 'chintokkong', 'text': '', 'title': '‘SQ117 owes me a glass of fresh milk’: The Singapore Airlines hijacking, 30 years on', 'score': 153, 'url': 'https://www.channelnewsasia.com/news/singapore/sq117-hijack-commando-singapore-airlines-14486940'}]
    
    #DB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["reddit"]
    if mycol.count_documents({}) != 0:
            # If database contains other day's data, clear it
            mycol.delete_many({})    
    if sgx_list:
        mycol.insert_many(sgx_list)
