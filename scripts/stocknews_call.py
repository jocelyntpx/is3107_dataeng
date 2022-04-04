import pymongo
import vanity
import pandas as pd
import json
from datetime import datetime, timedelta

def get_stocknews_data():
    doc = vanity.get_jsonparsed_data("https://stocknewsapi.com/api/v1?tickers=DBSDY,UOVEY,SINGY,SE,FXSG,EWS,MTGCF,STX,FUTU&items=50&token=cdxgrhebia7lvobqdvhfbhhk0wahvwlyo2e9kkmj")['data']

    # doc = [
    #     {
    #         "news_url": "https://investorplace.com/2022/03/7-death-cross-stocks-to-buy-when-others-are-selling/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/a/x/3de233-1146621-1230398-1288040.jpg",
    #         "title": "7 Death-Cross Stocks to Buy When Others Are Selling",
    #         "text": "While the ominous nature of the death cross spells doom, history suggests this could be an opportunity for stocks to buy. The post 7 Death-Cross Stocks to Buy When Others Are Selling appeared first on InvestorPlace.",
    #         "source_name": "InvestorPlace",
    #         "date": "Tue, 22 Mar 2022 09:46:20 -0400",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "DKNG",
    #             "EL",
    #             "INTU",
    #             "SE",
    #             "SHOP",
    #             "SHW",
    #             "TWLO"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/21/why-sea-limited-stock-crashed-by-7-monday/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/m/0/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6648252fstock-market-chart-crash-correction-buy-investment-planning-laptop-gettyjpgw700opresize-1222181-1286835.jpg",
    #         "title": "Why Sea Limited Stock Crashed by 7% Monday",
    #         "text": "HSBC still likes the stock -- but not as much as it used to.",
    #         "source_name": "The Motley Fool",
    #         "date": "Mon, 21 Mar 2022 15:57:58 -0400",
    #         "topics": [],
    #         "sentiment": "Negative",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://stockmarket.com/featured/4-top-communication-services-stocks-to-watch-in-march-2022-2022-03-21",
    #         "image_url": "https://cdn.snapi.dev/images/v1/g/o/asset-management30-1286790.jpg",
    #         "title": "4 Top Communication Services Stocks To Watch In March 2022",
    #         "text": "Could there be hidden gems among these communication services stocks?",
    #         "source_name": "Stockmarketcom",
    #         "date": "Mon, 21 Mar 2022 15:17:00 -0400",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "OMC",
    #             "SE",
    #             "TMUS",
    #             "ZM"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/21/3-stocks-down-50-or-more-that-wall-street-thinks-c/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6702602fcouple-with-woman-showing-man-ipadjpgw700opresize-1285570.jpg",
    #         "title": "3 Stocks Down 50% or More That Wall Street Thinks Could Nearly Double",
    #         "text": "They're beaten down -- but perhaps for not too much longer.",
    #         "source_name": "The Motley Fool",
    #         "date": "Mon, 21 Mar 2022 05:55:00 -0400",
    #         "topics": [],
    #         "sentiment": "Negative",
    #         "type": "Article",
    #         "tickers": [
    #             "SE",
    #             "SOFI",
    #             "TXG"
    #         ]
    #     },
    #     {
    #         "news_url": "https://investorplace.com/2022/03/solid-revenue-growth-wont-save-se-stock-as-net-losses-widen/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/l/h/445r3-945776-1063972-1213435-1284778.jpg",
    #         "title": "Solid Revenue Growth Won't Save Sea Limited Stock as Net Losses Widen",
    #         "text": "SE stock has been trending lower in 2022 despite the solid revenue growth. Don't trust claims that Sea Limited is a bargain now.",
    #         "source_name": "InvestorPlace",
    #         "date": "Fri, 18 Mar 2022 14:55:24 -0400",
    #         "topics": [
    #             "earnings"
    #         ],
    #         "sentiment": "Negative",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://seekingalpha.com/article/4496480-sea-limited-the-three-headed-monster",
    #         "image_url": "https://cdn.snapi.dev/images/v1/o/j/software4-1284625.jpg",
    #         "title": "Sea Limited: The Three-Headed Monster",
    #         "text": "Garena, Sea's only profitable segment, serves as a lifeline for its other two segments, but Bookings are expected to fall sharply in FY2022.",
    #         "source_name": "Seeking Alpha",
    #         "date": "Fri, 18 Mar 2022 13:01:14 -0400",
    #         "topics": [
    #             "paylimitwall"
    #         ],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/16/why-sea-limited-stock-is-soaring-today/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/d/c/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6707572fgettyimages-607922530jpgw700opresize-1280951.jpg",
    #         "title": "Why Sea Limited Stock Is Soaring Today",
    #         "text": "Investors were reacting to promising news for Chinese stocks.",
    #         "source_name": "The Motley Fool",
    #         "date": "Wed, 16 Mar 2022 13:39:33 -0400",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://seekingalpha.com/article/4495918-why-is-sea-limited-going-down-and-can-it-rebound",
    #         "image_url": "https://cdn.snapi.dev/images/v1/a/c/55t333-1156318-1280865.jpg",
    #         "title": "Why Is Sea Limited Going Down And Can It Rebound?",
    #         "text": "Sea Limited is down an astounding 75% from all-time highs.",
    #         "source_name": "Seeking Alpha",
    #         "date": "Wed, 16 Mar 2022 12:57:58 -0400",
    #         "topics": [
    #             "paylimitwall"
    #         ],
    #         "sentiment": "Negative",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/16/3-beaten-down-growth-stocks-billionaire-buying/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6702952fstock-trader-analyst-fund-manager-buy-sell-chart-decline-bear-market-smartphone-gettyjpgw700opresize-1279786.jpg",
    #         "title": "3 Beaten-Down Growth Stocks Billionaire Money Managers Can't Stop Buying",
    #         "text": "These fast-paced stocks have lost between 61% and 82% over the trailing 12 months.",
    #         "source_name": "The Motley Fool",
    #         "date": "Wed, 16 Mar 2022 05:21:00 -0400",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "CGC",
    #             "FVRR",
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/12/2-bargain-growth-stocks-you-can-confidently-buy-ri/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6695162fperson-shopping-online-looking-at-his-phonejpgw700opresize-1275366.jpg",
    #         "title": "2 Bargain Growth Stocks You Can Confidently Buy Right Now",
    #         "text": "Investors might want to consider buying the dip on these promising companies.",
    #         "source_name": "The Motley Fool",
    #         "date": "Sat, 12 Mar 2022 09:42:00 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "PUBM",
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/11/why-sea-limited-stock-flopped-on-friday/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/d/o/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6702402fgettyimages-1298319426jpgw700opresize-1275189.jpg",
    #         "title": "Why Sea Limited Stock Flopped on Friday",
    #         "text": "Yet another analyst cuts their price target on the company's shares.",
    #         "source_name": "The Motley Fool",
    #         "date": "Fri, 11 Mar 2022 18:50:08 -0500",
    #         "topics": [],
    #         "sentiment": "Negative",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.gurufocus.com/news/1663319/4-stocks-with-solid-financial-strength",
    #         "image_url": "https://cdn.snapi.dev/images/v1/s/9/iu2jed-729921-732545-1274913.jpg",
    #         "title": "4 Stocks With Solid Financial Strength",
    #         "text": "Benjamin Graham, the father of value investing, recommended investors look for stocks that have a current ratio higher than 2 and more working capital than long-term debt.",
    #         "source_name": "GuruFocus",
    #         "date": "Fri, 11 Mar 2022 14:45:51 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "AMAT",
    #             "AMD",
    #             "ATVI",
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://seekingalpha.com/article/4494643-sea-limited-spotlight-is-on-shopee-now",
    #         "image_url": "https://cdn.snapi.dev/images/v1/g/y/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f5795682fasian-smartphone-online-gaming-video-sea-limited-gettyjpegw700opresize-1202275-1273653.jpg",
    #         "title": "Sea Limited: Spotlight Is On Shopee Now",
    #         "text": "The importance of Garena is fading away and the spotlight is on Shopee.",
    #         "source_name": "Seeking Alpha",
    #         "date": "Thu, 10 Mar 2022 19:40:37 -0500",
    #         "topics": [
    #             "paylimitwall"
    #         ],
    #         "sentiment": "Neutral",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/10/why-shopify-sea-and-mercadolibre-stocks-crashed/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/5/o/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6699372f3-red-arrows-going-down-and-crashing-into-and-cracking-the-floorjpgw700opresize-1272730.jpg",
    #         "title": "Why Shopify, Sea, and MercadoLibre Stocks Crashed Today",
    #         "text": "Compared to Amazon, all other e-commerce stocks may come up short.",
    #         "source_name": "The Motley Fool",
    #         "date": "Thu, 10 Mar 2022 12:37:12 -0500",
    #         "topics": [],
    #         "sentiment": "Negative",
    #         "type": "Article",
    #         "tickers": [
    #             "MELI",
    #             "SHOP",
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.prnewswire.com/news-releases/shareholder-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-sea-limited---se-301499590.html",
    #         "image_url": "https://cdn.snapi.dev/images/v1/u/g/press16-1271269.jpg",
    #         "title": "SHAREHOLDER ALERT: Pomerantz Law Firm Investigates Claims On Behalf of Investors of Sea Limited - SE",
    #         "text": "NEW YORK, March 9, 2022 /PRNewswire/ -- Pomerantz LLP is investigating claims on behalf of investors of Sea Limited (\"Sea\" or the \"Company\") (NYSE: SE).  Such investors are advised to contact Robert S.",
    #         "source_name": "PRNewsWire",
    #         "date": "Wed, 09 Mar 2022 18:48:00 -0500",
    #         "topics": [
    #             "PressRelease",
    #             "Shareholder Alert"
    #         ],
    #         "sentiment": "Neutral",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/09/why-block-sea-limited-and-stoneco-skyrocketed-toda/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/o/d/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6697802fgettyimages-937126944jpgw700opresize-1270802.jpg",
    #         "title": "Why Block, Sea Limited, and StoneCo Skyrocketed Today",
    #         "text": "Falling oil prices and higher Treasury yields bode well for financial sector companies, especially beaten-down fintech stocks.",
    #         "source_name": "The Motley Fool",
    #         "date": "Wed, 09 Mar 2022 15:04:10 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "SE",
    #             "STNE",
    #             "SQ"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/09/3-top-gaming-stocks-to-watch-in-march/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6692662fonline-gaming-video-gettyjpegw700opresize-1270438.jpg",
    #         "title": "3 Top Gaming Stocks to Watch in March",
    #         "text": "The gaming sector has been battered, but investors should watch this trio of former highfliers.",
    #         "source_name": "The Motley Fool",
    #         "date": "Wed, 09 Mar 2022 11:30:00 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "RBLX",
    #             "SE",
    #             "SKLZ"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/09/this-global-e-commerce-trio-has-multibag-potential/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/5/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6688992fpointing-out-new-stock-picksjpgw700opresize-1269598.jpg",
    #         "title": "This Global E-Commerce Trio Offers Multibagger Potential",
    #         "text": "Buying and holding this discounted basket could help fund an early retirement.",
    #         "source_name": "The Motley Fool",
    #         "date": "Wed, 09 Mar 2022 07:00:00 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "CPNG",
    #             "MELI",
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://www.fool.com/investing/2022/03/09/3-top-e-commerce-stocks-to-buy-in-march/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6694452fgettyimages-1301007650jpgw700opresize-1269548.jpg",
    #         "title": "3 Top E-Commerce Stocks to Buy in March",
    #         "text": "E-commerce stocks have plunged because of fears over inflation and of economic reopening. But these long-term winners still have a lot of growth ahead of them.",
    #         "source_name": "The Motley Fool",
    #         "date": "Wed, 09 Mar 2022 06:30:00 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "AMZN",
    #             "FB",
    #             "SE"
    #         ]
    #     },
    #     {
    #         "news_url": "https://investorplace.com/2022/03/se-stock-is-oversold-and-priced-like-a-pre-pandemic-bargain/",
    #         "image_url": "https://cdn.snapi.dev/images/v1/g/s/software45-1269217.jpg",
    #         "title": "Sea Limited Is Oversold and Priced Like a Pre-Pandemic Bargain",
    #         "text": "SE stock has reached an inflection point and is set for upside amid robust earnings growth, resulting in an attractive valuation. The post Sea Limited Is Oversold and Priced Like a Pre-Pandemic Bargain appeared first on InvestorPlace.",
    #         "source_name": "InvestorPlace",
    #         "date": "Tue, 08 Mar 2022 18:52:10 -0500",
    #         "topics": [],
    #         "sentiment": "Positive",
    #         "type": "Article",
    #         "tickers": [
    #             "SE"
    #         ]
    #     }
    # ]

    df = pd.json_normalize(doc)
    df['datetime_created'] = [pd.to_datetime(x).tz_convert('Asia/Singapore').strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(x) else pd.NaT for x in df['date']]

    # df['date'] = [pd.to_datetime(x) if not pd.isna(x) else pd.NaT for x in df['datetime_created']]
    # df = df[df['date'] == (datetime.today() - timedelta(days=1)).date()]
    df.rename(columns={'source_name':'publisher','news_url':'url','tickers':'ticker'}, inplace=True)
    df['source'] = 'stocknews'
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
