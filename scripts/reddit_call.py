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
    reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=SECRET_TOKEN,
                     passticker=PASSticker, 
                     user_agent='TESTING praw accessAPI:v0.0.1 (by /u/Still_Statistician32)',
                     username=USERNAME)
    subreddit = reddit.subreddit('singapore')
    sgx_list = []
    # sgx_subreddit = iter('')
    start = time.time()
    for word in tickers_dict.keys():
        sgx_subreddit = subreddit.search(word)
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Singapore')
        for posts in sgx_subreddit:
            sgx_dict = {}
            # Convert UTC to GMT+8
            new_datetime = str(dt.datetime.fromtimestamp(posts.created))
            utc = datetime.strptime(new_datetime, '%Y-%m-%d %H:%M:%S')
            utc = utc.replace(tzinfo=from_zone)
            local = utc.astimezone(to_zone)
            local_dt = local.strftime('%Y-%m-%d %H:%M:%S')
            
            if (local_dt == (datetime.today() - timedelta(days=1)).date()):
                sgx_dict['datetime_created'] = local_dt
                sgx_dict['source'] = 'Reddit'
                ticker_list = []
                for ticker, name in tickers_dict.items():
                    if (ticker in posts.selftext.lower()) or (ticker in posts.title.lower()):
                        ticker_list.append(name)
                sgx_dict['ticker'] = ticker_list
                sgx_dict['publisher'] = str(posts.author)
                sgx_dict['text'] = posts.selftext
                sgx_dict['title'] = posts.title
                sgx_dict['score'] = posts.score
                sgx_dict['url'] = posts.url
                sgx_list.append(sgx_dict)
    end = time.time()
    print('Time execution duration (secs): ', end-start)
    print(sgx_list)

    sgx_list = [
    {
        "datetime_created":"2021-08-02 09:46:46",
        "source":"Reddit",
        "ticker":[
            "SPH",
            "Keppel"
        ],
        "publisher":"KingCWL",
        "text":"",
        "title":"Trading halts called for Keppel Corp, Keppel Reit, SPH and SPH Reit",
        "score":0,
        "url":"https://www.straitstimes.com/business/companies-markets/keppel-makes-34-billion-offer-to-take-sph-private-after-restructuring-of"
    },
    {
        "datetime_created":"2021-02-08 17:10:54",
        "source":"Reddit",
        "ticker":[
            "SIA"
        ],
        "publisher":"KingCWL",
        "text":"",
        "title":"Broker's take: SIA to benefit from air traffic recovery, say analysts",
        "score":7,
        "url":"https://www.businesstimes.com.sg/companies-markets/brokers-take-sia-to-benefit-from-air-traffic-recovery-say-analysts"
    },
    {
        "datetime_created":"2021-02-05 15:04:52",
        "source":"Reddit",
        "ticker":[
            "SIA"
        ],
        "publisher":"KingCWL",
        "text":"",
        "title":"SIA posts lower net loss of $142m in Q3",
        "score":4,
        "url":"https://www.straitstimes.com/business/sia-posts-lower-net-loss-of-142m-in-q3"
    },
    {
        "datetime_created":"2021-01-29 14:39:16",
        "source":"Reddit",
        "ticker":[
            "SIA"
        ],
        "publisher":"KingCWL",
        "text":"",
        "title":"SIA and SilkAir",
        "score":2,
        "url":"https://www.theedgesingapore.com/news/aviation/sia-fly-phuket-march-boeing-737-800-silkair-fully-integrate-sia-fy20212022"
    },
    {
        "datetime_created":"2021-03-08 11:21:45",
        "source":"Reddit",
        "ticker":[
            "SIA",
            "DBS"
        ],
        "publisher":"oceanus-medtecs",
        "text":"ALL IN CALL: Team Singapore, Let\\'s ALL Play our Part in Securing Singapore Future and Food Security. Further more UNLIKE INS Favorite [$DBS(D05.SI)](https://www.investingnote.com/stocks/SGX:D05) and [$SIA(C6L.SI)](https://www.investingnote.com/stocks/SGX:C6L) let by either foreigners or Greedy Locals, Let\\'s ALL SUPPORT Our LOCAL CEO and HOME GROWN Company. If not for yourself, do it for your CHILDREN AND GRANDDCHILDREN.  \n\n\nNote Oceanus has a STAKE in this.  \n\n\nPrawn farm scales new heights with high-tech vertical system  \n\n\nUp to 200kg of crustacean will be produced daily; firm may tap new govt fund as it looks to expand  \n\n\nFish and vegetable farming has already gone high-rise in land-scarce Singapore. Now, another type of farming has gone vertical.  \n\n\nWhen the first harvest from Universal Aquaculture\\'s Tuas South Link facility is ready come June, the sweet, juicy flesh of live vannamei prawns will be much easier to get hold of.  \n\n\nFor a start, the farm will be able to produce between 150kg and 200kg a day of the crustacean - also known as Pacific white shrimp, white-legged shrimp, king prawn, or bai xia.  \n\n\nBut as the high-tech system is modular and can be easily deployed at a larger industrial plot, chief executive Jeremy Ong said some 1,000kg of the prawns can be produced per day when the firm opens an additional site some time in the third quarter of next year.  \n\n\nUniversal Aquaculture is among the farms here that can benefit from the new $60 million Agri-Food Cluster Transformation Fund, the details of which were released last week during the debate over the budget of the Ministry of Sustainability and the Environment. It replaces the Agriculture Productivity Fund.  \n\n\nUnder the new fund, farmers looking to set up new sites or retrofit indoor spaces at industrial sites can also receive co-funding of up to $1.5 million to cover infrastructure and building costs, said the Singapore Food Agency, a unit under the ministry. This was not available previously.  \n\n\nThe new fund will also feature an expanded co-funding scope so farmers can use the money not just to boost yield but also, for instance, to bring in technology to reduce pollution and waste.  \n\n\nIt will also cover farms\\' expenses related to the upcoming Clean and Green Standard to be launched later this year, such as the purchase of equipment and certification-related fees.  \n\n\nMr Ong said: \"We are happy that the grant scope has expanded and are grateful for the opportunity to apply.\"  \n\n\nHe said transformation is key to Singapore meeting its \"30 by 30\" goal, which is to produce 30 per cent of the country\\'s nutritional needs by 2030. Currently, the nation produces less than 10 per cent of its own food.  \n\n\n\"It is painfully clear that we will not likely meet our 30 by 30 targets by using traditional farming methods,\" said Mr Ong.  \n\n\nHe added that the technology-upscaling component of the fund - which will provide co-funding support for the purchase of advanced farming technology solutions - is something his firm will consider.  \n\n\nBut he noted that the co-funding offer of 50 per cent of costs - or up to $700,000 - still \"falls far short of what we need to build the next farm\".  \nAt Universal Aquaculture\\'s current facility in Tuas South Link, prawns are reared in a six-tier system. The controlled environment means the farm does not have to use antibiotics on the creatures, which are also not exposed to pollutants such as microplastics or mercury.  \n\n\nTo reduce the energy requirements of a filtration system that relies on pumps to cleanse the water, Universal Aquaculture developed its own \"hybrid biological recirculation system\" - so the water can be reused in an energy-efficient way.  \nThis system harnesses the natural purifying abilities of beneficial bacteria and other aquatic plants, such as sea grapes that the firm can also sell.  \n\n\nProfessor William Chen, the Michael Fam chair professor in food science and technology at Nanyang Technological University, said it is \"excellent\" for farmers to be developing their own farming systems.  \n\n\n\"This is important as not all commercial technology can be directly adopted without retrofitting for our local context,\" he said.  \n\n\nContinued research and development may be helpful to improve the farming system, especially for novel technologies, he said.  \n\n\nSingapore Food Agency chief executive Lim Kok Thai said the new fund will support farms as they shift towards making the most of technology to overcome the country\\'s land and resource constraints.  \n\n\n\"Not only will this contribute towards our food security, it will create good jobs such as agriculture and aquaculture specialist roles for our people,\" he added.\n\n&#x200B;\n\n[https://www.straitstimes.com/singapore/environment/prawn-farm-scales-new-heights-with-high-tech-vertical-system?fbclid=IwAR2Sy-PTh8l-w9-z9eOz3ay6Cke9C2PTTI2wiadMMmRbSgOiXtb1mu3a8GI](https://www.straitstimes.com/singapore/environment/prawn-farm-scales-new-heights-with-high-tech-vertical-system?fbclid=IwAR2Sy-PTh8l-w9-z9eOz3ay6Cke9C2PTTI2wiadMMmRbSgOiXtb1mu3a8GI)\n\n&#x200B;\n\n&#x200B;\n\nhttps://preview.redd.it/tcb05cw23ql61.jpg?width=3869&format=pjpg&auto=webp&s=963172189b2c676e20e80f9bb6fa3b47b07a432e",
        "title":"OCEANUS: ALL-IN CALL, Once in a Lifetime but need to HOLD Diamond Hands. Min DOUBLE in 6 months.",
        "score":7,
        "url":"https://www.reddit.com/r/Sgxbets/comments/m06mh7/oceanus_allin_call_once_in_a_lifetime_but_need_to/"
    },
    {
        "datetime_created":"2021-02-04 12:32:58",
        "source":"Reddit",
        "ticker":[
            "SIA"
        ],
        "publisher":"oceanus-medtecs",
        "text":"I am going to start with the Concerns\n\n1. Valuation/Market Cap given run-up in share price\n\nThe concern really is Oceanus worth 1.5-2 Billion esp since many have done, it would be hard for Results to justify their PE ratio. Valid Concern, though read below. \n\n2. More Naysayers + Shortists which also means more Contra Buyers (i.e Speculation + Smart Alecs)\n\n70 Million Shorts YTD + More At Forum shouting down: The issue is we are NOT sure if Oceanus BB want to support, Long Retails have Limited Funds. Valid concern, if cannot hold, perhaps Sell? If got bullets, must have Strategy to Fight! 1st Half of the Day: Avoid the Battle. 2nd Half is where the Daily Battle Starts. If possible Try 4.38PM and each buy up as much as u can. then leave half to park at the price you buy. Say we manage to buy up 6.3. Then Block 6.3, force the shorts to cover 6.4 and beyond. If ONE day we strong enough, we play better block 6.3 and queue 6.5, make the shorts lose 2 pips. LAGI best is alot of Shorts queue say 6.6. End of the Day, we BUY up, force Naked Shorts, next day SGX BUY-IN + Make them Pay 1k SGD per day!\n\nWhat are the Good Catalysts? \n\n1. Macro Factors: Stimulus of US (Hot Money/Flush of Cash)\n\nBiden stimulus is more or less. Will this be good for the market? Yes liquidity, hot money.\n\n2. Impending Results: What to Look out For\n\nDon't expect results to be SO SO good to justify the current price. See the results in this Context:\n\nA. Results Backward Looking: It is Pandemic Results, if good = great, cause pandemic got good means no pandemic = great.\n\nB. Cyclical: Q1 which is NOW, is NOT reflected in the coming results, meaning this is a ADDED boost.\n\nLook out for\n\nC. Increase in Revenue/Profit %\n\nD. Are the results in line with EXITing SGX watchlist\n\nE. Forward Looking Statements\n\nF. Breakdown of Revenue as well as COSG\n\n3. SGX Watchlist: Inevitable, Signs are There (MAJOR FACTOR)\n\nCOMPANY Already HINT liao. PAP Top Star Join liao. Also Once Exit Watch List means BB can ENTER. Temasek, Ark Invest will ENTER Deep Tech + 2030 Food Security\n\n4. Rumours of Oceanus Abalone in PAP goodie bag to citizen \n\nIf true, Ah Kong support. See SIA: Ah kong have UNLIMITED MONEY and RULES to Favour who they want to save. \n\n5. Misunderstood Abalone Play + Misunderstood China Lockdown and No Abalone Eating \n\nSome claim China Lockdown and No Abalone Eating. That someone is a Boomer who reads Google headlines. I am in China, CNY in full Swing and ABALONE is a BIG THING. Please don't be a Boomer or Ostrich. \n\nNOT a Call to Buy because Price Up alot liao + Alot of Shortist lurking. if want to buy, must diamond hands.",
        "title":"$Oceanus^(579.SI) [Analysis: Both Sides]",
        "score":8,
        "url":"https://www.reddit.com/r/Sgxbets/comments/lc7kcd/oceanus579si_analysis_both_sides/"
    },
    {
        "datetime_created":"2021-03-09 15:49:34",
        "source":"Reddit",
        "ticker":[
            "OCBC"
        ],
        "publisher":"Beat-the-big-boys",
        "text":"I'm in at 1.358",
        "title":"Lion-OCBC Sec HSTECH, anyone?",
        "score":0,
        "url":"https://www.reddit.com/r/Sgxbets/comments/m11pvf/lionocbc_sec_hstech_anyone/"
    },
    {
        "datetime_created":"2021-02-05 08:51:27",
        "source":"Reddit",
        "ticker":[
            "DBS"
        ],
        "publisher":"oceanus-medtecs",
        "text":"Breaking $Oceanus\\^(579.SI) \n\n&#x200B;\n\nhttps://preview.redd.it/aez56pcy3kf61.jpg?width=2048&format=pjpg&auto=webp&s=611da05f40a7f32e50ea60b3440cb2a1df1c6fc1\n\nWith the pandemic crisis in 2020, it was a nudge for many companies, as they realise that they will need to evolve from past practices if we want to survive the pandemic.  For Oceanus, we have been constantly innovating since 2015. This allowed us to continue to grow our revenue and profit even in 2020. The journey has only just begun, and Oceanus is still evolving continuously, especially as we kickstart our 3-year plan of Tech-Up phase.  As the founder of an investment foundry focused on improving technologies in agriculture, food, and life sciences, David Friedberg knew the importance of improving the efficiency and economics of global food and agriculture markets. He says, \"Innovation is the only sustainable competitive advantage a company can have.\"  #OceanusGroup #sustainability #innovation #foodtech",
        "title":"Oceanus: Singapore's Tesla, Takeover DBS by 2025",
        "score":15,
        "url":"https://www.reddit.com/r/Sgxbets/comments/lcv64a/oceanus_singapores_tesla_takeover_dbs_by_2025/"
    },
    {
        "datetime_created":"2021-03-23 08:27:37",
        "source":"Reddit",
        "ticker":[
            "DBS"
        ],
        "publisher":"shareandstocks",
        "text":"",
        "title":"Singapore tech stocks ‘cheapest’ in Asean region: DBS | The Edge Singapore",
        "score":3,
        "url":"https://www.shareandstocks.com/singapore-tech-stocks-cheapest-in-asean-region-dbs-the-edge-singapore/"
    },
    {
        "datetime_created":"2021-03-05 16:24:35",
        "source":"Reddit",
        "ticker":[
            "DBS"
        ],
        "publisher":"shareandstocks",
        "text":"",
        "title":"Potential near-term relisting of ARA a ‘key’ catalyst for Straits Trading: DBS | The Edge Singapore",
        "score":2,
        "url":"https://www.shareandstocks.com/potential-near-term-relisting-of-ara-a-key-catalyst-for-straits-trading-dbs-the-edge-singapore/"
    },
    {
        "datetime_created":"2021-03-08 11:21:45",
        "source":"Reddit",
        "ticker":[
            "SIA",
            "DBS"
        ],
        "publisher":"oceanus-medtecs",
        "text":"ALL IN CALL: Team Singapore, Let\\'s ALL Play our Part in Securing Singapore Future and Food Security. Further more UNLIKE INS Favorite [$DBS(D05.SI)](https://www.investingnote.com/stocks/SGX:D05) and [$SIA(C6L.SI)](https://www.investingnote.com/stocks/SGX:C6L) let by either foreigners or Greedy Locals, Let\\'s ALL SUPPORT Our LOCAL CEO and HOME GROWN Company. If not for yourself, do it for your CHILDREN AND GRANDDCHILDREN.  \n\n\nNote Oceanus has a STAKE in this.  \n\n\nPrawn farm scales new heights with high-tech vertical system  \n\n\nUp to 200kg of crustacean will be produced daily; firm may tap new govt fund as it looks to expand  \n\n\nFish and vegetable farming has already gone high-rise in land-scarce Singapore. Now, another type of farming has gone vertical.  \n\n\nWhen the first harvest from Universal Aquaculture\\'s Tuas South Link facility is ready come June, the sweet, juicy flesh of live vannamei prawns will be much easier to get hold of.  \n\n\nFor a start, the farm will be able to produce between 150kg and 200kg a day of the crustacean - also known as Pacific white shrimp, white-legged shrimp, king prawn, or bai xia.  \n\n\nBut as the high-tech system is modular and can be easily deployed at a larger industrial plot, chief executive Jeremy Ong said some 1,000kg of the prawns can be produced per day when the firm opens an additional site some time in the third quarter of next year.  \n\n\nUniversal Aquaculture is among the farms here that can benefit from the new $60 million Agri-Food Cluster Transformation Fund, the details of which were released last week during the debate over the budget of the Ministry of Sustainability and the Environment. It replaces the Agriculture Productivity Fund.  \n\n\nUnder the new fund, farmers looking to set up new sites or retrofit indoor spaces at industrial sites can also receive co-funding of up to $1.5 million to cover infrastructure and building costs, said the Singapore Food Agency, a unit under the ministry. This was not available previously.  \n\n\nThe new fund will also feature an expanded co-funding scope so farmers can use the money not just to boost yield but also, for instance, to bring in technology to reduce pollution and waste.  \n\n\nIt will also cover farms\\' expenses related to the upcoming Clean and Green Standard to be launched later this year, such as the purchase of equipment and certification-related fees.  \n\n\nMr Ong said: \"We are happy that the grant scope has expanded and are grateful for the opportunity to apply.\"  \n\n\nHe said transformation is key to Singapore meeting its \"30 by 30\" goal, which is to produce 30 per cent of the country\\'s nutritional needs by 2030. Currently, the nation produces less than 10 per cent of its own food.  \n\n\n\"It is painfully clear that we will not likely meet our 30 by 30 targets by using traditional farming methods,\" said Mr Ong.  \n\n\nHe added that the technology-upscaling component of the fund - which will provide co-funding support for the purchase of advanced farming technology solutions - is something his firm will consider.  \n\n\nBut he noted that the co-funding offer of 50 per cent of costs - or up to $700,000 - still \"falls far short of what we need to build the next farm\".  \nAt Universal Aquaculture\\'s current facility in Tuas South Link, prawns are reared in a six-tier system. The controlled environment means the farm does not have to use antibiotics on the creatures, which are also not exposed to pollutants such as microplastics or mercury.  \n\n\nTo reduce the energy requirements of a filtration system that relies on pumps to cleanse the water, Universal Aquaculture developed its own \"hybrid biological recirculation system\" - so the water can be reused in an energy-efficient way.  \nThis system harnesses the natural purifying abilities of beneficial bacteria and other aquatic plants, such as sea grapes that the firm can also sell.  \n\n\nProfessor William Chen, the Michael Fam chair professor in food science and technology at Nanyang Technological University, said it is \"excellent\" for farmers to be developing their own farming systems.  \n\n\n\"This is important as not all commercial technology can be directly adopted without retrofitting for our local context,\" he said.  \n\n\nContinued research and development may be helpful to improve the farming system, especially for novel technologies, he said.  \n\n\nSingapore Food Agency chief executive Lim Kok Thai said the new fund will support farms as they shift towards making the most of technology to overcome the country\\'s land and resource constraints.  \n\n\n\"Not only will this contribute towards our food security, it will create good jobs such as agriculture and aquaculture specialist roles for our people,\" he added.\n\n&#x200B;\n\n[https://www.straitstimes.com/singapore/environment/prawn-farm-scales-new-heights-with-high-tech-vertical-system?fbclid=IwAR2Sy-PTh8l-w9-z9eOz3ay6Cke9C2PTTI2wiadMMmRbSgOiXtb1mu3a8GI](https://www.straitstimes.com/singapore/environment/prawn-farm-scales-new-heights-with-high-tech-vertical-system?fbclid=IwAR2Sy-PTh8l-w9-z9eOz3ay6Cke9C2PTTI2wiadMMmRbSgOiXtb1mu3a8GI)\n\n&#x200B;\n\n&#x200B;\n\nhttps://preview.redd.it/tcb05cw23ql61.jpg?width=3869&format=pjpg&auto=webp&s=963172189b2c676e20e80f9bb6fa3b47b07a432e",
        "title":"OCEANUS: ALL-IN CALL, Once in a Lifetime but need to HOLD Diamond Hands. Min DOUBLE in 6 months.",
        "score":6,
        "url":"https://www.reddit.com/r/Sgxbets/comments/m06mh7/oceanus_allin_call_once_in_a_lifetime_but_need_to/"
    },
    {
        "datetime_created":"2021-03-18 14:19:56",
        "source":"Reddit",
        "ticker":[
            "UOB"
        ],
        "publisher":"shareandstocks",
        "text":"",
        "title":"UOB Kay Hian initiates coverage on UMS Holdings with ‘buy’ rating, TP of $1.65 | The Edge Singapore",
        "score":3,
        "url":"https://www.shareandstocks.com/uob-kay-hian-initiates-coverage-on-ums-holdings-with-buy-rating-tp-of-1-65-the-edge-singapore/"
    },
    {
        "datetime_created":"2021-09-16 09:09:42",
        "source":"Reddit",
        "ticker":[
            "UOB"
        ],
        "publisher":"Gg-com992",
        "text":"I reproduce  the extract of an  impartial article written by  UOB kay Hian  dated 20th January2021. I urge retail investors like us  to do your own diligence . As of now, the factors highlighted   are still applicable if  not enhanced. . Nothing had changed in the modus operandi of Oceanus. The recent sparkling result enhanced and revalidated the points highlighted.   Follow the trend, the trend is your friend.  Don’t follow the nays Sayers. \nQuote\n The recent setting up of Season Global will enable Oceanus to\nattract MNC brands and expand its China distribution business in a big way. Oceanus\ntargets to build a foodtech company and to become a regional player.\n• New CEO, stronger shareholder and joining of a reputable independent director\nListed on the SGX since 2002, Oceanus Group (Oceanus) started as an abalone\nproducer. \nIn 2014, Oceanus experienced financial difficulties due to poor management and\nindustry challenges. Current CEO Peter Koh was a shareholder before he joined Oceanus\nat end-14. Peter has driven a strong turnaround as promised by growing revenue\nsignificantly, and he now aims to take Oceanus to a higher level with his wide business\nconnection and management track record. The key initiatives undertaken by Peter include:\na) cost cutting in Dec 14; b) clean-up operations in 2016; and c) strengthen the balance\nsheet in 2017 after reducing its debt to zero. Alacrity Investment Group (Alacrity) became\nOceanus’ largest shareholder in mid-20 after taking over the stake from a creditor group.\nAlacrity is an investment arm of an Indonesia conglomerate that has interest in the retail\nand logistics sector. It has long-term plans to help Oceanus expand its presence in the\naquaculture chain. In late-20, former minister Yaacob Ibrahim joined Oceanus as an\nindependent director, and this could strengthen corporate governance and show better\nconfidence in the company.\n• Season Global will penetrate China and deliver exponential growth. Oceanus’s 3Q20\nrevenue of Rmb135m has grown more than sixfold yoy, thanks to its strategy in building\nthe distribution business via the setting up of Season Global since Jan 20. The JV partner\nis a China FMCG conglomerate which has around 40 years of track record, more than\n1,000 stock keep units from foodstuffs to alcohol and generates around S$200m revenue.\nOceanus and the JV partner have invested S$20m, and significant growth is expected with\nthe opening up of markets and set-up of the e-commerce trading platform.\n• Targets to expand high-tech farming with regional presence. Oceanus envisions the\n2021-23 period to be its tech-up phase. COVID-19 has accelerated the demand for many\nmajor cities to build their own food supplies as a contingency plan. This has opened up\nmany JV opportunities in the ASEAN, China and the Middle East regions. To achieve its\ngoal of building a foodtech company with regional presence, Oceanus aims to establish\nintellectual properties, build a network of key partners and embark on a global deployment\nof Oceanus foodtech hubs. In Sep 20, Oceanus invested an undisclosed amount in\nUniversal Aquaculture, which has developed a novel shrimp farming facility in Singapore.\nThis could help develop in-house technology with a low capex business model. In Nov 20,\nOceanus signed an agreement with Hainan Raffles Group to set up the world’s first\nOceanus foodtech Hub in Hainan, China, a key aquaculture centre for shrimp and fish\nfarming in the region.\n\nNear-term key catalysts include:\n• Exiting from the SGX watch-list. Based on the profitability of Rmb6.1m achieved in\n9M20, Oceanus is on track to fulfil the condition to exit from the SGX watch-list. In Jan 21,\nOceanus announced that it is no longer in the SGX list that requires mandatory quarterly\nfinancial reporting. This is an upgrade of confidence from SGX as it is loosening its\nreporting requirement for Oceanus.\n• Exponential revenue and earnings growth from Season Global. Since establishing\nSeason Global JV in Jan 20, the revenue and net profit of Oceanus has grown\nsignificantly. In 3Q20, Oceanus’ revenue grew by 626% yoy (+276% qoq) and net profit\nmade a turnaround to Rmb2.5m from a loss of Rmb1.4m earlier. Oceanus expects this\ndistribution division to drive significant growth with the opening up of more markets,\nespecially in China.\n• Further expansion of aquaculture businesses. The COVID-19 pandemic has\naccelerated the demand for many major cities to build their own food supplies. This could\nopen up more opportunities for Oceanus to deploy its foodtech hubs which utilise high-tech\nand vertical farming in key cities across China, ASEAN and the Middle East.\n\nkey catalysts for price up trend \n• Exiting from the SGX watch-list.  Ticked YES \n• Exponential revenue and earnings growth from Season Global Ticked yes \n• Further expansion of aquaculture businesses. The COVID-19 pandemic has\naccelerated the demand for many major cities to build their own food supplies. This could\nopen up more opportunities for Oceanus to deploy its foodtech hubs which utilise high-tech\nand vertical farming in key cities across China, ASEAN and the Middle East. Ticked yes \n\nThere were comments about Fed taperwing QE resulting interest rate spikes. Let me assure you it will affect drastically  the high valued stocks with high dividend yields.  Why because of the big capital outlay . You can put in the bank to earn higher interest.\nIt will affect less Penny stocks like Oceanus  why. As long as Oceanus is fundamentally viable, It will enhance investing in Oceanus because of low capital outlay and the returns from your investment will outweigh you putting the meagre amount in the bank. There will be shift of focus to penny stock with good potential and fundamental.",
        "title":"Oceanus stocks",
        "score":3,
        "url":"https://www.reddit.com/r/Sgxbets/comments/pp39bh/oceanus_stocks/"
    },
    {
        "datetime_created":"2021-02-20 17:31:58",
        "source":"Reddit",
        "ticker":[
            "UOB"
        ],
        "publisher":"DexterT-",
        "text":"This will be my view on Oceanus Group and why I think it is still currently bullish. Please take my opinions with a pinch of salt and do your own due diligence.  \n\n\n***Bullish Opinion***\n\n1. Oceanus Group recently received a query from SGX because of their 11% increase in price movement and to which, Oceanus Group replies to being unaware of any possible reasons that might cause the price surge. However, based on my limited time in research, I have come up with these 3 potential reasons.  \n\n\n**Bullish Graph** \n\nhttps://preview.redd.it/b5v1smfcpli61.jpg?width=933&format=pjpg&auto=webp&s=30526a7446d09680dc7957162e37548442901406\n\nBased on the graph above, we can see that there is 2 strong support forming at **$0.062** and **$0.067.** With such a strong support forming and investors consolidating, it tends to spark up with any positive news.  \n\n\n**Joey Choy Analysis**\n\nJoey Choy from Philip Securities posted a video on 2 SG Penny Stocks that are below $0.20 with more uptrend potential. Those 2 SG Penny Stocks are Oceanus Group and Jiutian Chemical. With Joey Choy's reputation as Singapore's renowned mentor and as one of the Top Tier Remisiers and Trader, he might have some influence through his analyst.\n\nLink: [https://www.youtube.com/watch?v=PU6EOxCASIQ&t=647s](https://www.youtube.com/watch?v=PU6EOxCASIQ&t=647s)\n\n&#x200B;\n\n**Terenece Cao Partnering**\n\nTerence's home-based F&B business sets up Mee Siam delivery and partners with nine Singaporean farms to sell their produce on its site. The first of these being Oceanus Group's abalone.\n\nLink: [https://www.8days.sg/eatanddrink/newsandopening/terence-cao-sets-up-mee-siam-delivery-biz-gets-700-enquiries-on-14225762](https://www.8days.sg/eatanddrink/newsandopening/terence-cao-sets-up-mee-siam-delivery-biz-gets-700-enquiries-on-14225762)\n\n&#x200B;\n\n2. Since 2018, Oceanus Group has constantly generated increasing profits year after year. The amazing growth of **200% - 300%**  per year due to their **strategize 4 pillars of growth**. **Gaining revenue from 4 different sectors, Aquaculture, Distribution, Services, and Innovation**. Their latest revenue between 2019 to Q1-Q3 2020, shows an increase of 305%. ( Exponential revenue and earnings growth )\n\n&#x200B;\n\n3. As CEO Peter Koh joins Oceanus Group in 2014, he **managed to turn the company around** from being heavily in debt to absolutely **no debt** by 2017. This allows Oceanus Group to achieve their first 'Clean' audit opinion in Nine Years. This could only be done after successfully resolving all legacy issues that have caused disclaimer of opinions from its auditors between FY2011 to FY2017.\n\nLink: [https://oceanus.com.sg/oceanus-achieves-first-clean-audit-opinion-in-nine-years/](https://oceanus.com.sg/oceanus-achieves-first-clean-audit-opinion-in-nine-years/)\n\n&#x200B;\n\n4. Seeing Oceanus Group's growth potential, **former Minister Yaccob Ibrahim joins Oceanus Group as an independent director** and invested in the company in 2020. With former Minister Yaccob Ibrahim involvement in the company, Oceanus Group will indefinitely move faster and stronger forward with his skills and knowledge in his sector.\n\nLink: [https://oceanus.com.sg/former-minister-yaacob-ibrahim-joins-oceanus-as-independent-director/](https://oceanus.com.sg/former-minister-yaacob-ibrahim-joins-oceanus-as-independent-director/)\n\n&#x200B;\n\n5. Oceanus Group has plans to apply out of SGX watchlist in April 2021 after auditing their FY2020 results. The result on whether they have successfully exited out of SGX watchlist will be announced in Q3/4 2021. Looking at how Oceanus Group has progressed over the years and their confidence in applying out of SGX watchlist, I feel there will be positive news in Q3/4 2021.\n\n&#x200B;\n\nhttps://preview.redd.it/pumr6ppqpli61.jpg?width=1701&format=pjpg&auto=webp&s=c1bfc37b207f25badd265b1b7aa1b10812293d24\n\nhttps://preview.redd.it/51ske6lrpli61.jpg?width=1701&format=pjpg&auto=webp&s=89cf6e593c4ed2cac530c6bc0ff8ff67b50b4bd7\n\nhttps://preview.redd.it/1skhl2dspli61.jpg?width=1701&format=pjpg&auto=webp&s=ddd570a358dcb1716b7d7bf36d6ce7946f360355\n\nLink: [https://www.facebook.com/OceanusGroupLimited/posts/877066023043380](https://www.facebook.com/OceanusGroupLimited/posts/877066023043380)\n\n&#x200B;\n\n6. Because of the pandemic crisis in 2020, it was a nudge for many companies. Oceanus Group realizes that they will need to evolve from past practices to survive the pandemic and so they did. They have been constantly innovating since 2015. This allowed Oceanus Group to continue to grow revenue and profit even in 2020. The journey has only just begun, especially as they kickstart their 3-year plan of Tech-Up phase.\n\n&#x200B;\n\nhttps://preview.redd.it/gy8692hupli61.jpg?width=2048&format=pjpg&auto=webp&s=593526b587e122199bcef971633c3aafce19dc2e\n\nAn exciting project that Oceanus has was their Aquapolis City project with 2 other companies, Shaw Investment Holdings, and China Construction Seventh Engineering Division. The project was created to tackle food security concerns from governments around the world. It is a sea-based hi-tech aquaponics farm that aims to be the solution to food security and safety in Singapore and beyond. Although Oceanus Group has not released any updates or progress of the Aquapolis project, I hope to hear more about it in their 3-year tech-up phase.\n\nLink: [https://www.businesstimes.com.sg/companies-markets/oceanus-partners-shaw-investment-holdings-chinese-construction-firm-to-enhance](https://www.businesstimes.com.sg/companies-markets/oceanus-partners-shaw-investment-holdings-chinese-construction-firm-to-enhance)\n\n&#x200B;\n\n7. Oceanus Group is set to release its Q4 2020 earnings report in February. I am confident that their earnings report will be good as having a good consistent financial profit year over year is one of the criteria to be able to apply out of SGX watchlist.\n\nhttps://preview.redd.it/ujomp0nwpli61.jpg?width=2048&format=pjpg&auto=webp&s=6e315f9db12280b62f585ac7a26db151f7579999\n\n&#x200B;\n\n8. I came upon Oceanus Market Depth data while researching and noticed something interesting. The amount of shares at the sell queue is decreasing over time compared to when it was priced at $0.03. When the share price was at $0.03, the selling volume was at close to 40-50 million shares, and as of 19/02/2020, the share price at $0.076 was around 20-30 million shares. I am not sure about you, but this tells me that many Oceanus Group supporters are holding on to their shares because they believe in the company. \n\n&#x200B;\n\nhttps://preview.redd.it/fqfk9fozpli61.jpg?width=631&format=pjpg&auto=webp&s=47e04879afc239e623285461ec6a47b5dd4b6e90\n\n&#x200B;\n\n***Investment***\n\nOceanus Group in 2020 has been making strategic investments towards the food-tech space. Investment such as:  \n\n\n1. Investment in Universal Aquaculture for Deep Tech Indoor Prawn breeding.\n\nLink: [https://www.businesstimes.com.sg/companies-markets/oceanus-invests-in-deep-tech-firm-to-breed-prawns](https://www.businesstimes.com.sg/companies-markets/oceanus-invests-in-deep-tech-firm-to-breed-prawns)\n\n2. Signed an agreement with Hainan Raffles Group, to set up the world's first Oceanus FoodTech Hub in Hainan. A key aquaculture center for shrimp and fish farming in the region.\n\nLink: [https://links.sgx.com/1.0.0/corporate-announcements/Q98FNYLCZ2E1YRFB/669685e053e41e000255387677e65a2f6919e620ef5c6b240ce4eb1a489ba10d?fbclid=IwAR38wSvIJMLFq\\_KUBYI0nmhTuNodYfg22ztw-z58JpcVCDyLA6ibWb-OYGM](https://links.sgx.com/1.0.0/corporate-announcements/Q98FNYLCZ2E1YRFB/669685e053e41e000255387677e65a2f6919e620ef5c6b240ce4eb1a489ba10d?fbclid=IwAR38wSvIJMLFq_KUBYI0nmhTuNodYfg22ztw-z58JpcVCDyLA6ibWb-OYGM)\n\n&#x200B;\n\n***Upcoming Near-term key Catalyst***  \n\n\n1. **Q4 2020 Results**. The Q4 2020 results will be released this coming February and in my opinion, it will no doubt be great as compared to the previous quarter.\n\n&#x200B;\n\n2. **Exiting from SGX watch-list**. Based on the profitability achieved in Q1-Q3 2020, Oceanus is on track to fulfill the condition to exit from SGX watch-list. This is an upgrade of confidence from SGX as it is loosening its reporting requirement for Oceanus.\n\n&#x200B;\n\n3. **Exponential revenue and earnings growth from Season Global**. Since establishing Season Global JV in Jan 2020, the revenue of Oceanus Group has grown significantly. In Q1-Q3 2020, Oceanus Group's revenue grew by 626% year over year ( +276% quarter over quarter ) and made a turnaround from a loss to profit. \n\n&#x200B;\n\n4. **Further expansion of aquaculture businesses**. The Covid-19 pandemic has accelerated the demand for many major cities to build their own food supplies. The could open up more opportunities for Oceanus to deploy its food tech hubs in key cities across China, ASEAN, and the Middle East.\n\n&#x200B;\n\n***Bearish Opinion***\n\nOf course, there will definitely be some bearish opinions as there is bullish.  \n\n\n1. Oceanus Group's valuation is a whopping $1.822 billion as of this writing. Its share price is at $0.075 on 19/02/2020 closing.   \n\n\n2. Oceanus Group's P/B ratio is at 76.27x as compared to its fair value and price relative to the market.\n\nLink: [https://www.theedgesingapore.com/capital/right-timing/caution-warranted-penny-stocks-overbought-highs-sti-slumps](https://www.theedgesingapore.com/capital/right-timing/caution-warranted-penny-stocks-overbought-highs-sti-slumps)  \n\n\nBased on the above numbers, Oceanus Group is overvalued as compared to other counters such as First Resources Ltd, Bumitama Agri Ltd, and Indofood Agri Resources Ltd to name a few. However, I would not use these numbers to value Oceanus Group as it is a growth company. We invest based on how we see the company's future, and from how I see it, Oceanus Group is en route to greater growth and earnings with strong fundamentals that are built since 2014.\n\n&#x200B;\n\n***Other Links***  \n\n\nTo those who would love to know more about Oceanus Group or where I get my research from, below are a few links provided for your convenience.  \n\n\n**UOB KayHian Analyst Report on Oceanus Group**\n\nLink: [https://research.sginvestors.io/2021/01/oceanus-group-uob-kay-hian-research-2021-01-20.html](https://research.sginvestors.io/2021/01/oceanus-group-uob-kay-hian-research-2021-01-20.html)  \n\n\n**89.3 Money FM interview on Oceanus Group CEO Peter Koh**\n\nLink: [https://omny.fm/shows/money-fm-893/driving-a-resilient-aquaculture-business-amid-covi?fbclid=IwAR2YoxNBFyWbjDwkaVmAeCBDYYLvRP40hC5KttwRnBWPhgJd5IMSrSxYvQA#description](https://omny.fm/shows/money-fm-893/driving-a-resilient-aquaculture-business-amid-covi?fbclid=IwAR2YoxNBFyWbjDwkaVmAeCBDYYLvRP40hC5KttwRnBWPhgJd5IMSrSxYvQA#description)  \n\n\n**Oceanus Facebook (Oceanus post updates on their progress)**\n\nLink: [https://www.facebook.com/OceanusGroupLimited](https://www.facebook.com/OceanusGroupLimited)\n\n&#x200B;\n\n**Disclaimer**: All content on this post is for informational & educational purposes only, and shouldn't be taken as personalized financial advice. Always do your own due diligence before investing. Cheers!",
        "title":"Oceanus still Bullish",
        "score":10,
        "url":"https://www.reddit.com/r/Sgxbets/comments/lo3o1x/oceanus_still_bullish/"
    },
    {
        "datetime_created":"2021-04-01 19:09:04",
        "source":"Reddit",
        "ticker":[
            "Sembcorp"
        ],
        "publisher":"Breadskinjinhojiak",
        "text":"Why pamp today",
        "title":"Sembcorp Marine",
        "score":4,
        "url":"https://www.reddit.com/r/Sgxbets/comments/mhsyuq/sembcorp_marine/"
    },
    {
        "datetime_created":"2021-02-21 12:16:23",
        "source":"Reddit",
        "ticker":[
            "Sembcorp",
            "Keppel"
        ],
        "publisher":"oceanus-medtecs",
        "text":"$Oceanus\\^(579.SI) Final Piece of Due Diligence by Bro Greg till Results. ALL-IN: ONCE IN A LIFE TIME. Backed by Singapore Government at ALL Levels. \n\n  \n12 Growth Companies, Bro Greg give u Sum-of-Parts valuation and i LOW-BALL each company say 200 million, that's 2.4 Billion which means Fair Value 0.10 or TEN CENTS. Now 7.5 cents got much more room!! Huat gao gao! \n\n  \nPaying 2 Billion+++ for 4 Pillars of Growth and 12 Companies\n\n  \n1. Aquaculture under this not just Abalone or Prawn but also High Value Fish like TUNA (cue Japan Tuna 1 Tuna for 1 Million SGD) and Lobsters (high value)\n\n  \nAquaculture has always been a cornerstone pillar of Oceanus Group’s business since its inception, with a focus on addressing global food security. Strong emphasis is placed on sustainable practices and the use of cutting-edge aquaculture technologies.\n\n  \n**Milestones after 2017**\n\n  \nOceanus Group has one of the world’s largest land-based abalone farm with teams in China and Indonesia ensuring seafood is sustainably sourced and food safety standards are met.  \nWe have expanded our product range to fish and crustaceans and have exported to Singapore, China, Japan and USA.\n\n  \nCompany A under Aquaculture: Oceanus China\n\n  \nOceanus Group (China) Aquaculture Ltd (“OCA”), a fully owned China subsidiary of the Group, operates the abalone hatchery farms in China. Located along the sea in Fo Tan town of Fujian, China, it has a total of 6669 tanks spread across its 39.18 hectare land.\n\n  \nWith 135 farm workers, it is capable of spawning over 200 million juvenile abalones each season with a production capacity of 133.38 million juveniles every year. Being a land-based aquaculture facility, the abalone juveniles’ breeding environment is carefully controlled to encourage their growth, survival and propagation so as to deliver consistent supply.\n\n  \nOceanus Group has also entered into strategic contract farming arrangements with aquaculture farmers which allows full utilisation of all of its tanks and maximise profits.  \nCompany B under Aquaculture: Asia Fisheries\n\n  \nAsia Fisheries focuses on the expanding the group's aquaculture business further down the value chain, by bring quality wild-caught and farmed seafood products to customers around the world, including customers in Singapore, USA, UK, Australia and Japan  \n\n\n#### Our Products\n\nWe deliver a variety of fresh seafood such as Fishes, Molluscs and Crustaceans  \n[https://asia-fisheries.com/](https://asia-fisheries.com/)\n\n  \nCompany C under Aquaculture: Universal Aquaculture\n\n  \nUniversal aquaculture was founded in 2020 by a team of Aquaculture enthusiasts, with combined experience of 30 years in the Aquaculture industry. Our mission is to build the global food systems of tomorrow, using environmentally sound and sustainable food production methods.\n\n  \nOur focus is on the intensive production of vannamei, in a fully controlled indoor environment using our industry-leading poly-culture hybrid re-circulating Aquaculture system with bio-floc technology.\n\n  \nCompany D under Aquaculture: Pelamis Group backed by AUSTRALIAN GOVT\n\n  \nThe Australian Tuna Fisheries \\xa0are a proven sustainable resource that is strictly controlled by the Australian Government (***AFMA)*** on behalf of the Australian community.\\xa0This controls extends to tuna species:WTBF - Western Tuna & Billfish FisherySBTF - Southern Bluefin Tuna FisherySJTF - Skipjack Tuna FisheryETBF - Western Tuna & Billfish Fishery  \n2. DISTRIBUTION BIZ\n\n  \nOceanus Group leverages upon its existing corporate presence and trading network globally to strengthen its position across the value chain – from raw materials to consumer goods.\n\n  \n**Milestones after 2017**  \nOver the last couple of years, we have successfully increase our FMCG range to more than 2000 different products. We have also increase our global footprint to 16 countries worldwide.\n\n  \nCompany A under Distribution: Season Global Trading is a FMCG company. We pride ourselves as a nimble and resourceful company. Covering Major Segments in: Alcohol, Cosmetics, Snacks, Seafood, Lifestyle Products\n\n  \nSeason Global Trading was conceived in partnership with Season Hong International Trading, a Chinese conglomerate with over 40 years of experience in the global consumer goods distribution market.\n\n  \nCompany B: Singapore Farmer  the one WE ALL BUY and Terence Cao all use!\n\n  \nCompany C: Xiamen Oceanus  \n3. Distribution Services backed by Singapore and Cambodian Govt\n\n  \nOceanus Group’s in-house capabilities in aquaculture consulting, marketing and branding are also offered to third parties. By serving as profit centres wherever possible, these services boost the overall productivity and profitability of Oceanus Group.\n\n  \n**Milestones after 2017**  \nOur award winning subsidiary, AP Media has spearheaded high profile projects both locally and overseas, such as the digitalisation Singapore’s history 200 years before Sir Stamford Raffles, live streaming of Singapore National Day parade 2019 and Art-Fest 2020 (Celebrating 55 years of diplomatic relationship between Singapore and Cambodia)\n\n  \n1. AP Media\n\n  \nClients include $Keppel Corp(BN4.SI) $Sembcorp Ind(U96.SI) Sime Darby $ST Engineering(S63.SI) etc POWERHOUSES also National Art Gallery, A\\*Star  \nalso in VR Facebook Occulus Media Marketing.  \nMARTECH: Marketing Tech  \n2. RESOLUT MEDIA  \n3. SCOPI  \n4. INNOVATION\n\n## Oceanus Group stays ahead of the curve with innovative research and development\n\nIn line with Oceanus Group’s ongoing strategy to pursue cutting-edge aquaculture R&D alongside its industry partners and institutions, an innovation centre was established in July 2017.\n\n  \n**Milestones after 2017**Oceanus has set up of Oceanus Oceanic Institute in Zhangpu & Oceanus Innovation Centre @ Temasek Polytechnic. We also have ongoing research collaboration with Temasek Polytechnic and Republic Polytechnic on juvenile abalone growth  \nCOMPANY 1Oceanus Oceanic Institute (OOI) was established as Oceanus Group Limited’s Research and Development arm.\n\n  \nLocated at Oceanus Group farm in China, OOI is responsible for the development and implementation of various risk management and protocols for all Oceanus Group’s farm, including it technology and system.\n\n  \nin pursuit of sustainable food technologies, from enhancing yield to quality of assets. We endeavor to shape the future of farming with a strong focus on food security through sustainable R&D and research-based farming  \nCOMPANY 2: OCEANUS TECH",
        "title":"OCEANUS: 4 PILLARS OF GROWTH, 12 GROWTH COMPANIES FOR THE PRICE OF 1, FAIR VALUE 0.10 SGD. ALL IN. BACKED BY AH KONG AT ALL LEVELS.",
        "score":4,
        "url":"https://www.reddit.com/r/Sgxbets/comments/loor1u/oceanus_4_pillars_of_growth_12_growth_companies/"
    },
    {
        "datetime_created":"2021-08-02 09:46:46",
        "source":"Reddit",
        "ticker":[
            "SPH",
            "Keppel"
        ],
        "publisher":"KingCWL",
        "text":"",
        "title":"Trading halts called for Keppel Corp, Keppel Reit, SPH and SPH Reit",
        "score":0,
        "url":"https://www.straitstimes.com/business/companies-markets/keppel-makes-34-billion-offer-to-take-sph-private-after-restructuring-of"
    },
    {
        "datetime_created":"2021-02-21 12:16:23",
        "source":"Reddit",
        "ticker":[
            "Sembcorp",
            "Keppel"
        ],
        "publisher":"oceanus-medtecs",
        "text":"$Oceanus\\^(579.SI) Final Piece of Due Diligence by Bro Greg till Results. ALL-IN: ONCE IN A LIFE TIME. Backed by Singapore Government at ALL Levels. \n\n  \n12 Growth Companies, Bro Greg give u Sum-of-Parts valuation and i LOW-BALL each company say 200 million, that's 2.4 Billion which means Fair Value 0.10 or TEN CENTS. Now 7.5 cents got much more room!! Huat gao gao! \n\n  \nPaying 2 Billion+++ for 4 Pillars of Growth and 12 Companies\n\n  \n1. Aquaculture under this not just Abalone or Prawn but also High Value Fish like TUNA (cue Japan Tuna 1 Tuna for 1 Million SGD) and Lobsters (high value)\n\n  \nAquaculture has always been a cornerstone pillar of Oceanus Group’s business since its inception, with a focus on addressing global food security. Strong emphasis is placed on sustainable practices and the use of cutting-edge aquaculture technologies.\n\n  \n**Milestones after 2017**\n\n  \nOceanus Group has one of the world’s largest land-based abalone farm with teams in China and Indonesia ensuring seafood is sustainably sourced and food safety standards are met.  \nWe have expanded our product range to fish and crustaceans and have exported to Singapore, China, Japan and USA.\n\n  \nCompany A under Aquaculture: Oceanus China\n\n  \nOceanus Group (China) Aquaculture Ltd (“OCA”), a fully owned China subsidiary of the Group, operates the abalone hatchery farms in China. Located along the sea in Fo Tan town of Fujian, China, it has a total of 6669 tanks spread across its 39.18 hectare land.\n\n  \nWith 135 farm workers, it is capable of spawning over 200 million juvenile abalones each season with a production capacity of 133.38 million juveniles every year. Being a land-based aquaculture facility, the abalone juveniles’ breeding environment is carefully controlled to encourage their growth, survival and propagation so as to deliver consistent supply.\n\n  \nOceanus Group has also entered into strategic contract farming arrangements with aquaculture farmers which allows full utilisation of all of its tanks and maximise profits.  \nCompany B under Aquaculture: Asia Fisheries\n\n  \nAsia Fisheries focuses on the expanding the group's aquaculture business further down the value chain, by bring quality wild-caught and farmed seafood products to customers around the world, including customers in Singapore, USA, UK, Australia and Japan  \n\n\n#### Our Products\n\nWe deliver a variety of fresh seafood such as Fishes, Molluscs and Crustaceans  \n[https://asia-fisheries.com/](https://asia-fisheries.com/)\n\n  \nCompany C under Aquaculture: Universal Aquaculture\n\n  \nUniversal aquaculture was founded in 2020 by a team of Aquaculture enthusiasts, with combined experience of 30 years in the Aquaculture industry. Our mission is to build the global food systems of tomorrow, using environmentally sound and sustainable food production methods.\n\n  \nOur focus is on the intensive production of vannamei, in a fully controlled indoor environment using our industry-leading poly-culture hybrid re-circulating Aquaculture system with bio-floc technology.\n\n  \nCompany D under Aquaculture: Pelamis Group backed by AUSTRALIAN GOVT\n\n  \nThe Australian Tuna Fisheries \\xa0are a proven sustainable resource that is strictly controlled by the Australian Government (***AFMA)*** on behalf of the Australian community.\\xa0This controls extends to tuna species:WTBF - Western Tuna & Billfish FisherySBTF - Southern Bluefin Tuna FisherySJTF - Skipjack Tuna FisheryETBF - Western Tuna & Billfish Fishery  \n2. DISTRIBUTION BIZ\n\n  \nOceanus Group leverages upon its existing corporate presence and trading network globally to strengthen its position across the value chain – from raw materials to consumer goods.\n\n  \n**Milestones after 2017**  \nOver the last couple of years, we have successfully increase our FMCG range to more than 2000 different products. We have also increase our global footprint to 16 countries worldwide.\n\n  \nCompany A under Distribution: Season Global Trading is a FMCG company. We pride ourselves as a nimble and resourceful company. Covering Major Segments in: Alcohol, Cosmetics, Snacks, Seafood, Lifestyle Products\n\n  \nSeason Global Trading was conceived in partnership with Season Hong International Trading, a Chinese conglomerate with over 40 years of experience in the global consumer goods distribution market.\n\n  \nCompany B: Singapore Farmer  the one WE ALL BUY and Terence Cao all use!\n\n  \nCompany C: Xiamen Oceanus  \n3. Distribution Services backed by Singapore and Cambodian Govt\n\n  \nOceanus Group’s in-house capabilities in aquaculture consulting, marketing and branding are also offered to third parties. By serving as profit centres wherever possible, these services boost the overall productivity and profitability of Oceanus Group.\n\n  \n**Milestones after 2017**  \nOur award winning subsidiary, AP Media has spearheaded high profile projects both locally and overseas, such as the digitalisation Singapore’s history 200 years before Sir Stamford Raffles, live streaming of Singapore National Day parade 2019 and Art-Fest 2020 (Celebrating 55 years of diplomatic relationship between Singapore and Cambodia)\n\n  \n1. AP Media\n\n  \nClients include $Keppel Corp(BN4.SI) $Sembcorp Ind(U96.SI) Sime Darby $ST Engineering(S63.SI) etc POWERHOUSES also National Art Gallery, A\\*Star  \nalso in VR Facebook Occulus Media Marketing.  \nMARTECH: Marketing Tech  \n2. RESOLUT MEDIA  \n3. SCOPI  \n4. INNOVATION\n\n## Oceanus Group stays ahead of the curve with innovative research and development\n\nIn line with Oceanus Group’s ongoing strategy to pursue cutting-edge aquaculture R&D alongside its industry partners and institutions, an innovation centre was established in July 2017.\n\n  \n**Milestones after 2017**Oceanus has set up of Oceanus Oceanic Institute in Zhangpu & Oceanus Innovation Centre @ Temasek Polytechnic. We also have ongoing research collaboration with Temasek Polytechnic and Republic Polytechnic on juvenile abalone growth  \nCOMPANY 1Oceanus Oceanic Institute (OOI) was established as Oceanus Group Limited’s Research and Development arm.\n\n  \nLocated at Oceanus Group farm in China, OOI is responsible for the development and implementation of various risk management and protocols for all Oceanus Group’s farm, including it technology and system.\n\n  \nin pursuit of sustainable food technologies, from enhancing yield to quality of assets. We endeavor to shape the future of farming with a strong focus on food security through sustainable R&D and research-based farming  \nCOMPANY 2: OCEANUS TECH",
        "title":"OCEANUS: 4 PILLARS OF GROWTH, 12 GROWTH COMPANIES FOR THE PRICE OF 1, FAIR VALUE 0.10 SGD. ALL IN. BACKED BY AH KONG AT ALL LEVELS.",
        "score":4,
        "url":"https://www.reddit.com/r/Sgxbets/comments/loor1u/oceanus_4_pillars_of_growth_12_growth_companies/"
    }
    ]
    
    #DB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["reddit"]
    if mycol.count_documents({}) != 0:
            # If database contains other day's data, clear it
            mycol.delete_many({})    
    if sgx_list:
        mycol.insert_many(sgx_list)
