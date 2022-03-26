from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta  
import datetime as dt
import pandas as pd
import requests

import praw
import pymongo


USERNAME = 'Still_Statistician32'
PASSWORD = 'BD99cjOO'
CLIENT_ID = 'CSwmabTf7mzgHTmg2zynPg'
SECRET_TOKEN = '9VSTmChi6sqT5JCct1ha8Y3ctxKeVg'

my_tickers = ['HSI','China']


def get_reddit_data():
    '''
    reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=SECRET_TOKEN,
                     password=PASSWORD, 
                     user_agent='TESTING praw accessAPI:v0.0.1 (by /u/Still_Statistician32)',
                     username=USERNAME)

    subreddit = reddit.subreddit('sgxbets')

    sgx_subreddit = subreddit.search(my_tickers, limit = 20, sort = 'new')

    sgx_list = []
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
            for word in my_tickers:
                if word in posts.selftext:
                    ticker_list.append(word)
            sgx_dict['ticker'] = ticker_list
            sgx_dict['publisher'] = str(posts.author)
            sgx_dict['text'] = posts.selftext
            sgx_dict['title'] = posts.title
            sgx_dict['score'] = posts.score
            sgx_dict['url'] = posts.url
            sgx_list.append(sgx_dict)
    '''


    sgx_list = [
        {
            "datetime_created":"2022-03-21 13:51:42",
            "source":"Reddit",
            "ticker":[
                "HSI",
                "China"
            ],
            "publisher":"City_Index",
            "text":"The Hang Seng Index seemed like it could have formed a V-bottom after last week’s rally as speculation of additional stimulus in China helped erase losses from earlier in the week.\n\nHSI managed to break back above the March 2020 lows near 21,100, and now needs to hold this level as support before targeting the key May 2020 support line around 22,500. This will likely depend on the market’s risk sentiment in the coming days, which could get a boost from Hong Kong easing travel restrictions earlier today, as well as lockdown in the tech-hub, Shenzhen, being lifted. \n\nHowever, the decision to leave the loan prime rate unchanged today seems to have disappointed traders who were hoping for further policy easing. It will also be important to watch how the situation between the US and China develops, as well as the regulatory crackdowns, both of which have the potential to drag Chinese shares lower. At the time of writing, HSI is down over 1.4% and retesting that 21,100 support level. \n\nAll trading carries risk, but it should be interesting to see if the index can avoid a close below this level and start a new leg higher, or if it's poised to attempt another downside breakout in the coming days.",
            "title":"Is the HSI ready for a new leg higher?",
            "score":2,
            "url":"https://www.reddit.com/r/Sgxbets/comments/tj4px5/is_the_hsi_ready_for_a_new_leg_higher/"
        },
        {
            "datetime_created":"2022-02-16 14:07:34",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"City_Index",
            "text":"China’s efforts in ramping up their presence in the metaverse industry, and further policy easing by the PBOC could prove to be beneficial for the Hang Seng Index over the coming days. \n\nThe index is trading 1.2% higher at the time of writing, as the latest inflation data signalled the likelihood of further monetary stimulus by Chinese officials. The Hang Seng has held up relatively well given the underperformance by its largest holdings over the last. If global sentiment for equities can now continue to improve, allowing markets to build on this current bounce, it could result in the Hang Seng rallying to retesting that key 25k level, and target a sustained break above. \n\nHowever, tensions in Eastern Europe are far from over, and with markets continually repricing the odds of increasingly hawkish major central banks, risk-off sentiment could quickly return amongst investors. This would likely spark another round of selling, leaving the Hang Seng exposed to another leg lower, and a continuation of its long standing downtrend. \n\nAll trading carries risk, but this definitely looks like one to keep an eye on at the moment.",
            "title":"Can the Hang Seng break $25k in the coming days?",
            "score":3,
            "url":"https://www.reddit.com/r/Sgxbets/comments/stoosh/can_the_hang_seng_break_25k_in_the_coming_days/"
        },
        {
            "datetime_created":"2022-02-09 14:29:19",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"City_Index",
            "text":"Chinese stocks have underperformed so far in 2022, but yesterday’s rumours of state-backed funds stepping into the market might just be the key to reigniting equities. \n\nThe China A50 has been trending lower since its high in December, but managed to bounce near the key support level at 14500 coming from the lows in mid-2021. The index is broadly higher today as the news of the state looking to support the market seems to have boosted bullish sentiment. If the A50 can now manage a close above Monday’s highs and downtrend resistance just above 15140, it could potentially confirm a reversal and open the door for a sustained leg higher. \n\nHowever, it’s important to note that the Chinese economy and stock market is still in an extremely precarious position. A failed breakout or rejection at the current levels could easily swing momentum back in favour of the bears, and drag the index lower to retest 14500 support. \n\nAll trading carries risk, but this should be an interesting one to watch as the news develops.",
            "title":"Can the China A50 form a bullish reversal and rally?",
            "score":2,
            "url":"https://www.reddit.com/r/Sgxbets/comments/so6qor/can_the_china_a50_form_a_bullish_reversal_and/"
        },
        {
            "datetime_created":"2022-01-28 14:29:26",
            "source":"Reddit",
            "ticker":[
                "HSI",
                "China"
            ],
            "publisher":"City_Index",
            "text":"The Hang Seng Index looked poised for a rally last week after breaking a confluence of resistance levels around 24,400. But, bulls failed to hold these levels as losses accelerated across global equity markets over the last few days.\n\nHowever, there is still potential for the rally to resume. With the Fed meeting now out of the way, focus could shift back towards China’s policy easing designed to stimulate the economy. Doing so might allow the HSI to form a swing low at the current levels, and start another leg higher. \n\nWith that in mind, it should be noted that monetary policy speculation isn’t fully behind us yet, with other major central banks still scheduled to meet over the coming days. If we see them begin to mirror the Fed’s hawkishness, volatility will likely continue during the early days of February, and with the index currently testing the key level near 23,600, it could be at risk of a deeper pullback. \n\nAll trading carries risk, but it will be interesting to see which direction the Hang Seng goes from here.",
            "title":"Will the Hang Seng rally get back on track?",
            "score":3,
            "url":"https://www.reddit.com/r/Sgxbets/comments/sek7kg/will_the_hang_seng_rally_get_back_on_track/"
        },
        {
            "datetime_created":"2021-09-16 09:09:42",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"Gg-com992",
            "text":"I reproduce  the extract of an  impartial article written by  UOB kay Hian  dated 20th January2021. I urge retail investors like us  to do your own diligence . As of now, the factors highlighted   are still applicable if  not enhanced. . Nothing had changed in the modus operandi of Oceanus. The recent sparkling result enhanced and revalidated the points highlighted.   Follow the trend, the trend is your friend.  Don’t follow the nays Sayers. \nQuote\n The recent setting up of Season Global will enable Oceanus to\nattract MNC brands and expand its China distribution business in a big way. Oceanus\ntargets to build a foodtech company and to become a regional player.\n• New CEO, stronger shareholder and joining of a reputable independent director\nListed on the SGX since 2002, Oceanus Group (Oceanus) started as an abalone\nproducer. \nIn 2014, Oceanus experienced financial difficulties due to poor management and\nindustry challenges. Current CEO Peter Koh was a shareholder before he joined Oceanus\nat end-14. Peter has driven a strong turnaround as promised by growing revenue\nsignificantly, and he now aims to take Oceanus to a higher level with his wide business\nconnection and management track record. The key initiatives undertaken by Peter include:\na) cost cutting in Dec 14; b) clean-up operations in 2016; and c) strengthen the balance\nsheet in 2017 after reducing its debt to zero. Alacrity Investment Group (Alacrity) became\nOceanus’ largest shareholder in mid-20 after taking over the stake from a creditor group.\nAlacrity is an investment arm of an Indonesia conglomerate that has interest in the retail\nand logistics sector. It has long-term plans to help Oceanus expand its presence in the\naquaculture chain. In late-20, former minister Yaacob Ibrahim joined Oceanus as an\nindependent director, and this could strengthen corporate governance and show better\nconfidence in the company.\n• Season Global will penetrate China and deliver exponential growth. Oceanus’s 3Q20\nrevenue of Rmb135m has grown more than sixfold yoy, thanks to its strategy in building\nthe distribution business via the setting up of Season Global since Jan 20. The JV partner\nis a China FMCG conglomerate which has around 40 years of track record, more than\n1,000 stock keep units from foodstuffs to alcohol and generates around S$200m revenue.\nOceanus and the JV partner have invested S$20m, and significant growth is expected with\nthe opening up of markets and set-up of the e-commerce trading platform.\n• Targets to expand high-tech farming with regional presence. Oceanus envisions the\n2021-23 period to be its tech-up phase. COVID-19 has accelerated the demand for many\nmajor cities to build their own food supplies as a contingency plan. This has opened up\nmany JV opportunities in the ASEAN, China and the Middle East regions. To achieve its\ngoal of building a foodtech company with regional presence, Oceanus aims to establish\nintellectual properties, build a network of key partners and embark on a global deployment\nof Oceanus foodtech hubs. In Sep 20, Oceanus invested an undisclosed amount in\nUniversal Aquaculture, which has developed a novel shrimp farming facility in Singapore.\nThis could help develop in-house technology with a low capex business model. In Nov 20,\nOceanus signed an agreement with Hainan Raffles Group to set up the world’s first\nOceanus foodtech Hub in Hainan, China, a key aquaculture centre for shrimp and fish\nfarming in the region.\n\nNear-term key catalysts include:\n• Exiting from the SGX watch-list. Based on the profitability of Rmb6.1m achieved in\n9M20, Oceanus is on track to fulfil the condition to exit from the SGX watch-list. In Jan 21,\nOceanus announced that it is no longer in the SGX list that requires mandatory quarterly\nfinancial reporting. This is an upgrade of confidence from SGX as it is loosening its\nreporting requirement for Oceanus.\n• Exponential revenue and earnings growth from Season Global. Since establishing\nSeason Global JV in Jan 20, the revenue and net profit of Oceanus has grown\nsignificantly. In 3Q20, Oceanus’ revenue grew by 626% yoy (+276% qoq) and net profit\nmade a turnaround to Rmb2.5m from a loss of Rmb1.4m earlier. Oceanus expects this\ndistribution division to drive significant growth with the opening up of more markets,\nespecially in China.\n• Further expansion of aquaculture businesses. The COVID-19 pandemic has\naccelerated the demand for many major cities to build their own food supplies. This could\nopen up more opportunities for Oceanus to deploy its foodtech hubs which utilise high-tech\nand vertical farming in key cities across China, ASEAN and the Middle East.\n\nkey catalysts for price up trend \n• Exiting from the SGX watch-list.  Ticked YES \n• Exponential revenue and earnings growth from Season Global Ticked yes \n• Further expansion of aquaculture businesses. The COVID-19 pandemic has\naccelerated the demand for many major cities to build their own food supplies. This could\nopen up more opportunities for Oceanus to deploy its foodtech hubs which utilise high-tech\nand vertical farming in key cities across China, ASEAN and the Middle East. Ticked yes \n\nThere were comments about Fed taperwing QE resulting interest rate spikes. Let me assure you it will affect drastically  the high valued stocks with high dividend yields.  Why because of the big capital outlay . You can put in the bank to earn higher interest.\nIt will affect less Penny stocks like Oceanus  why. As long as Oceanus is fundamentally viable, It will enhance investing in Oceanus because of low capital outlay and the returns from your investment will outweigh you putting the meagre amount in the bank. There will be shift of focus to penny stock with good potential and fundamental.",
            "title":"Oceanus stocks",
            "score":3,
            "url":"https://www.reddit.com/r/Sgxbets/comments/pp39bh/oceanus_stocks/"
        },
        {
            "datetime_created":"2021-05-24 11:51:03",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"valuehunter69",
            "text":"Share price going up despite no announcements. Their main asset project in China is now under dispute. If the arbitration is against the company, the NAV will be significantly affected.",
            "title":"Is KOP a pump and dump?",
            "score":1,
            "url":"https://www.reddit.com/r/Sgxbets/comments/njovrs/is_kop_a_pump_and_dump/"
        },
        {
            "datetime_created":"2021-03-06 16:53:41",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"sg-ev",
            "text":"They have a OCS group doing chemical trading in China. \nFy20 revenue hit USD 400 millions. \n\nI reckon they will be able to grow this piece of pie in fy21.\n\nStay tune for this Penny.",
            "title":"Abundance",
            "score":2,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lyxpjj/abundance/"
        },
        {
            "datetime_created":"2021-02-27 10:24:40",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"oceanus-medtecs",
            "text":"Finally had the time to look through the report and cut the BS online. \n\nFull Year Revenue: 91,692 Million \n\n4th Quarter ALONE Revenue: 56,766 Million \n\nFull Yer Net Profit: 8,646 Million\n\n4th Quarter ALONE Net Profit: 7,438 Million \n\nProjecting Future Earnings (ULTRA conservative)\n\nQ1 2021 (CNY Effect): Revenue 88 Million est, Net Profit 11 Million (1 to 8 ratio from above)\n\nQ2-Q4 (conservative I take 10% above Q42020): Revenue 174 Million, Net Profit 23 Million \n\nTotal Projected Ultra Conservative: 262 Million Revenue, 34 Million Net Profit!\n\nOther Catalyst from the Report you may have missed (please note esp Point 1 and 3\\]\n\n1. CROWN Jewel Tech Play Investment: Universal Aquaculture Key Words: HIGHLY SCALABLE + EASILY REPLICATED GLOBALLY\n\nAdditionally, in line with the Group’s investment in deep tech indoor farming, Oceanus has invested in Universal Aquaculture Pte Ltd (“Universal Aquaculture”), a deep tech indoor company, in September 2020. Universal Aquaculture’s vertical farming capabilities, which enables the production of 300 tonnes of seafood per annum with a farm size of 0.28 hectares, are also highly scalable which can be easily replicated globally for sustainable urban food production.\n\nAlso BONUS for those who do Homework: Go Facebook, search Universal Aquaculture! In Feb during CNY they hinted \"WATCH THIS SPACE, we are releasing Something EXCITING SOON\" Greg Suspects this will be HUGE HUGE HUGE!\n\n2. Distribution Contributes Insane 74 Million Revenue and Growing for China and SEA given demand for Seafood and FMCG Products!\n\nIn Distribution, the Group has expanded and will continue to build upon its product range to over 2,000 FMCG products, with a focus on an expansion on frozen meat and fresh seafood products. Meanwhile, the Group’s subsidiary, Season Global Trading Pte. Ltd. (“SGTPL”), has gained significant traction in the key markets of China and Southeast Asia and will continue to expand its global presence. Going forward, Oceanus will continue to leverage on its global distribution network, supported by an integrated suite of logistics and supply chain services. This will help the Group cement its position in matters over food supply chain and addressing food security.\n\n3. Exiting Watchlist reaches the FINAL STEP and is ALMOST GUARANTEED (99.999999999%): \n\nMr Koh concluded, “We are pleased to have made good progress on our three year expansion plan which we embarked on in 2018, to build a resilient and profitable position for Oceanus. We are now focused on completing the FINAL STEP in SATISFYING the Financial Exit Criteria.”\n\n4. China Hainan Partnership\n\nHainan Raffles Group (“海南 莱佛士油田基地服务有限公司”), to set up the world’s first Oceanus FoodTech Hub in Hainan, China, a key aquaculture centre for shrimp and fish farming in the region. Hainan Raffles Group is a Chinese conglomerate which operates across diverse industries such as trading, real estate, offshore services, training and education. \n\nOceanus FoodTech Hub will be located within the Hainan Laocheng Economic Development Zone, China’s fourth comprehensive free trade zone. During the first phase, Oceanus FoodTech Hub will produce approximately 200 tonnes of shrimp for the first year of production before gradually increasing to approximately 1,000 tonnes of shrimp in the following years.\n\n5. Tech-Up Play \n\n“To ‘tech-up’ our operations for the next lap, Oceanus Group will focus on applying deep tech strategies to supplement our businesses, thereby creating additional growth for the Group, and enhancing food security in the process.\n\n“Notably, in 2020, we have made good progress in the development of IPs and the building up of a good network of key partners for our next growth phase. Through partnerships with Hainan Raffles Group and Universal Aquaculture, we have set up the world’s first Oceanus FoodTech Hub in Hainan, and separately, invested in a deep tech farm in Singapore.”",
            "title":"OCEANUS Learn to Read Report Properly [Result within a Result: INSANELY Good Q4 Result hidden by Full Year Presentation of Results + Here's the Kicker: Q4 traditionally been tje weakest quarter, traditionally best quarter has been Q1 for CNY]",
            "score":8,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lte1da/oceanus_learn_to_read_report_properly_result/"
        },
        {
            "datetime_created":"2021-02-21 12:16:23",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"oceanus-medtecs",
            "text":"$Oceanus\\^(579.SI) Final Piece of Due Diligence by Bro Greg till Results. ALL-IN: ONCE IN A LIFE TIME. Backed by Singapore Government at ALL Levels. \n\n  \n12 Growth Companies, Bro Greg give u Sum-of-Parts valuation and i LOW-BALL each company say 200 million, that's 2.4 Billion which means Fair Value 0.10 or TEN CENTS. Now 7.5 cents got much more room!! Huat gao gao! \n\n  \nPaying 2 Billion+++ for 4 Pillars of Growth and 12 Companies\n\n  \n1. Aquaculture under this not just Abalone or Prawn but also High Value Fish like TUNA (cue Japan Tuna 1 Tuna for 1 Million SGD) and Lobsters (high value)\n\n  \nAquaculture has always been a cornerstone pillar of Oceanus Group’s business since its inception, with a focus on addressing global food security. Strong emphasis is placed on sustainable practices and the use of cutting-edge aquaculture technologies.\n\n  \n**Milestones after 2017**\n\n  \nOceanus Group has one of the world’s largest land-based abalone farm with teams in China and Indonesia ensuring seafood is sustainably sourced and food safety standards are met.  \nWe have expanded our product range to fish and crustaceans and have exported to Singapore, China, Japan and USA.\n\n  \nCompany A under Aquaculture: Oceanus China\n\n  \nOceanus Group (China) Aquaculture Ltd (“OCA”), a fully owned China subsidiary of the Group, operates the abalone hatchery farms in China. Located along the sea in Fo Tan town of Fujian, China, it has a total of 6669 tanks spread across its 39.18 hectare land.\n\n  \nWith 135 farm workers, it is capable of spawning over 200 million juvenile abalones each season with a production capacity of 133.38 million juveniles every year. Being a land-based aquaculture facility, the abalone juveniles’ breeding environment is carefully controlled to encourage their growth, survival and propagation so as to deliver consistent supply.\n\n  \nOceanus Group has also entered into strategic contract farming arrangements with aquaculture farmers which allows full utilisation of all of its tanks and maximise profits.  \nCompany B under Aquaculture: Asia Fisheries\n\n  \nAsia Fisheries focuses on the expanding the group's aquaculture business further down the value chain, by bring quality wild-caught and farmed seafood products to customers around the world, including customers in Singapore, USA, UK, Australia and Japan  \n\n\n#### Our Products\n\nWe deliver a variety of fresh seafood such as Fishes, Molluscs and Crustaceans  \n[https://asia-fisheries.com/](https://asia-fisheries.com/)\n\n  \nCompany C under Aquaculture: Universal Aquaculture\n\n  \nUniversal aquaculture was founded in 2020 by a team of Aquaculture enthusiasts, with combined experience of 30 years in the Aquaculture industry. Our mission is to build the global food systems of tomorrow, using environmentally sound and sustainable food production methods.\n\n  \nOur focus is on the intensive production of vannamei, in a fully controlled indoor environment using our industry-leading poly-culture hybrid re-circulating Aquaculture system with bio-floc technology.\n\n  \nCompany D under Aquaculture: Pelamis Group backed by AUSTRALIAN GOVT\n\n  \nThe Australian Tuna Fisheries \\xa0are a proven sustainable resource that is strictly controlled by the Australian Government (***AFMA)*** on behalf of the Australian community.\\xa0This controls extends to tuna species:WTBF - Western Tuna & Billfish FisherySBTF - Southern Bluefin Tuna FisherySJTF - Skipjack Tuna FisheryETBF - Western Tuna & Billfish Fishery  \n2. DISTRIBUTION BIZ\n\n  \nOceanus Group leverages upon its existing corporate presence and trading network globally to strengthen its position across the value chain – from raw materials to consumer goods.\n\n  \n**Milestones after 2017**  \nOver the last couple of years, we have successfully increase our FMCG range to more than 2000 different products. We have also increase our global footprint to 16 countries worldwide.\n\n  \nCompany A under Distribution: Season Global Trading is a FMCG company. We pride ourselves as a nimble and resourceful company. Covering Major Segments in: Alcohol, Cosmetics, Snacks, Seafood, Lifestyle Products\n\n  \nSeason Global Trading was conceived in partnership with Season Hong International Trading, a Chinese conglomerate with over 40 years of experience in the global consumer goods distribution market.\n\n  \nCompany B: Singapore Farmer  the one WE ALL BUY and Terence Cao all use!\n\n  \nCompany C: Xiamen Oceanus  \n3. Distribution Services backed by Singapore and Cambodian Govt\n\n  \nOceanus Group’s in-house capabilities in aquaculture consulting, marketing and branding are also offered to third parties. By serving as profit centres wherever possible, these services boost the overall productivity and profitability of Oceanus Group.\n\n  \n**Milestones after 2017**  \nOur award winning subsidiary, AP Media has spearheaded high profile projects both locally and overseas, such as the digitalisation Singapore’s history 200 years before Sir Stamford Raffles, live streaming of Singapore National Day parade 2019 and Art-Fest 2020 (Celebrating 55 years of diplomatic relationship between Singapore and Cambodia)\n\n  \n1. AP Media\n\n  \nClients include $Keppel Corp(BN4.SI) $Sembcorp Ind(U96.SI) Sime Darby $ST Engineering(S63.SI) etc POWERHOUSES also National Art Gallery, A\\*Star  \nalso in VR Facebook Occulus Media Marketing.  \nMARTECH: Marketing Tech  \n2. RESOLUT MEDIA  \n3. SCOPI  \n4. INNOVATION\n\n## Oceanus Group stays ahead of the curve with innovative research and development\n\nIn line with Oceanus Group’s ongoing strategy to pursue cutting-edge aquaculture R&D alongside its industry partners and institutions, an innovation centre was established in July 2017.\n\n  \n**Milestones after 2017**Oceanus has set up of Oceanus Oceanic Institute in Zhangpu & Oceanus Innovation Centre @ Temasek Polytechnic. We also have ongoing research collaboration with Temasek Polytechnic and Republic Polytechnic on juvenile abalone growth  \nCOMPANY 1Oceanus Oceanic Institute (OOI) was established as Oceanus Group Limited’s Research and Development arm.\n\n  \nLocated at Oceanus Group farm in China, OOI is responsible for the development and implementation of various risk management and protocols for all Oceanus Group’s farm, including it technology and system.\n\n  \nin pursuit of sustainable food technologies, from enhancing yield to quality of assets. We endeavor to shape the future of farming with a strong focus on food security through sustainable R&D and research-based farming  \nCOMPANY 2: OCEANUS TECH",
            "title":"OCEANUS: 4 PILLARS OF GROWTH, 12 GROWTH COMPANIES FOR THE PRICE OF 1, FAIR VALUE 0.10 SGD. ALL IN. BACKED BY AH KONG AT ALL LEVELS.",
            "score":4,
            "url":"https://www.reddit.com/r/Sgxbets/comments/loor1u/oceanus_4_pillars_of_growth_12_growth_companies/"
        },
        {
            "datetime_created":"2021-02-20 17:31:58",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"DexterT-",
            "text":"This will be my view on Oceanus Group and why I think it is still currently bullish. Please take my opinions with a pinch of salt and do your own due diligence.  \n\n\n***Bullish Opinion***\n\n1. Oceanus Group recently received a query from SGX because of their 11% increase in price movement and to which, Oceanus Group replies to being unaware of any possible reasons that might cause the price surge. However, based on my limited time in research, I have come up with these 3 potential reasons.  \n\n\n**Bullish Graph** \n\nhttps://preview.redd.it/b5v1smfcpli61.jpg?width=933&format=pjpg&auto=webp&s=30526a7446d09680dc7957162e37548442901406\n\nBased on the graph above, we can see that there is 2 strong support forming at **$0.062** and **$0.067.** With such a strong support forming and investors consolidating, it tends to spark up with any positive news.  \n\n\n**Joey Choy Analysis**\n\nJoey Choy from Philip Securities posted a video on 2 SG Penny Stocks that are below $0.20 with more uptrend potential. Those 2 SG Penny Stocks are Oceanus Group and Jiutian Chemical. With Joey Choy's reputation as Singapore's renowned mentor and as one of the Top Tier Remisiers and Trader, he might have some influence through his analyst.\n\nLink: [https://www.youtube.com/watch?v=PU6EOxCASIQ&t=647s](https://www.youtube.com/watch?v=PU6EOxCASIQ&t=647s)\n\n&#x200B;\n\n**Terenece Cao Partnering**\n\nTerence's home-based F&B business sets up Mee Siam delivery and partners with nine Singaporean farms to sell their produce on its site. The first of these being Oceanus Group's abalone.\n\nLink: [https://www.8days.sg/eatanddrink/newsandopening/terence-cao-sets-up-mee-siam-delivery-biz-gets-700-enquiries-on-14225762](https://www.8days.sg/eatanddrink/newsandopening/terence-cao-sets-up-mee-siam-delivery-biz-gets-700-enquiries-on-14225762)\n\n&#x200B;\n\n2. Since 2018, Oceanus Group has constantly generated increasing profits year after year. The amazing growth of **200% - 300%**  per year due to their **strategize 4 pillars of growth**. **Gaining revenue from 4 different sectors, Aquaculture, Distribution, Services, and Innovation**. Their latest revenue between 2019 to Q1-Q3 2020, shows an increase of 305%. ( Exponential revenue and earnings growth )\n\n&#x200B;\n\n3. As CEO Peter Koh joins Oceanus Group in 2014, he **managed to turn the company around** from being heavily in debt to absolutely **no debt** by 2017. This allows Oceanus Group to achieve their first 'Clean' audit opinion in Nine Years. This could only be done after successfully resolving all legacy issues that have caused disclaimer of opinions from its auditors between FY2011 to FY2017.\n\nLink: [https://oceanus.com.sg/oceanus-achieves-first-clean-audit-opinion-in-nine-years/](https://oceanus.com.sg/oceanus-achieves-first-clean-audit-opinion-in-nine-years/)\n\n&#x200B;\n\n4. Seeing Oceanus Group's growth potential, **former Minister Yaccob Ibrahim joins Oceanus Group as an independent director** and invested in the company in 2020. With former Minister Yaccob Ibrahim involvement in the company, Oceanus Group will indefinitely move faster and stronger forward with his skills and knowledge in his sector.\n\nLink: [https://oceanus.com.sg/former-minister-yaacob-ibrahim-joins-oceanus-as-independent-director/](https://oceanus.com.sg/former-minister-yaacob-ibrahim-joins-oceanus-as-independent-director/)\n\n&#x200B;\n\n5. Oceanus Group has plans to apply out of SGX watchlist in April 2021 after auditing their FY2020 results. The result on whether they have successfully exited out of SGX watchlist will be announced in Q3/4 2021. Looking at how Oceanus Group has progressed over the years and their confidence in applying out of SGX watchlist, I feel there will be positive news in Q3/4 2021.\n\n&#x200B;\n\nhttps://preview.redd.it/pumr6ppqpli61.jpg?width=1701&format=pjpg&auto=webp&s=c1bfc37b207f25badd265b1b7aa1b10812293d24\n\nhttps://preview.redd.it/51ske6lrpli61.jpg?width=1701&format=pjpg&auto=webp&s=89cf6e593c4ed2cac530c6bc0ff8ff67b50b4bd7\n\nhttps://preview.redd.it/1skhl2dspli61.jpg?width=1701&format=pjpg&auto=webp&s=ddd570a358dcb1716b7d7bf36d6ce7946f360355\n\nLink: [https://www.facebook.com/OceanusGroupLimited/posts/877066023043380](https://www.facebook.com/OceanusGroupLimited/posts/877066023043380)\n\n&#x200B;\n\n6. Because of the pandemic crisis in 2020, it was a nudge for many companies. Oceanus Group realizes that they will need to evolve from past practices to survive the pandemic and so they did. They have been constantly innovating since 2015. This allowed Oceanus Group to continue to grow revenue and profit even in 2020. The journey has only just begun, especially as they kickstart their 3-year plan of Tech-Up phase.\n\n&#x200B;\n\nhttps://preview.redd.it/gy8692hupli61.jpg?width=2048&format=pjpg&auto=webp&s=593526b587e122199bcef971633c3aafce19dc2e\n\nAn exciting project that Oceanus has was their Aquapolis City project with 2 other companies, Shaw Investment Holdings, and China Construction Seventh Engineering Division. The project was created to tackle food security concerns from governments around the world. It is a sea-based hi-tech aquaponics farm that aims to be the solution to food security and safety in Singapore and beyond. Although Oceanus Group has not released any updates or progress of the Aquapolis project, I hope to hear more about it in their 3-year tech-up phase.\n\nLink: [https://www.businesstimes.com.sg/companies-markets/oceanus-partners-shaw-investment-holdings-chinese-construction-firm-to-enhance](https://www.businesstimes.com.sg/companies-markets/oceanus-partners-shaw-investment-holdings-chinese-construction-firm-to-enhance)\n\n&#x200B;\n\n7. Oceanus Group is set to release its Q4 2020 earnings report in February. I am confident that their earnings report will be good as having a good consistent financial profit year over year is one of the criteria to be able to apply out of SGX watchlist.\n\nhttps://preview.redd.it/ujomp0nwpli61.jpg?width=2048&format=pjpg&auto=webp&s=6e315f9db12280b62f585ac7a26db151f7579999\n\n&#x200B;\n\n8. I came upon Oceanus Market Depth data while researching and noticed something interesting. The amount of shares at the sell queue is decreasing over time compared to when it was priced at $0.03. When the share price was at $0.03, the selling volume was at close to 40-50 million shares, and as of 19/02/2020, the share price at $0.076 was around 20-30 million shares. I am not sure about you, but this tells me that many Oceanus Group supporters are holding on to their shares because they believe in the company. \n\n&#x200B;\n\nhttps://preview.redd.it/fqfk9fozpli61.jpg?width=631&format=pjpg&auto=webp&s=47e04879afc239e623285461ec6a47b5dd4b6e90\n\n&#x200B;\n\n***Investment***\n\nOceanus Group in 2020 has been making strategic investments towards the food-tech space. Investment such as:  \n\n\n1. Investment in Universal Aquaculture for Deep Tech Indoor Prawn breeding.\n\nLink: [https://www.businesstimes.com.sg/companies-markets/oceanus-invests-in-deep-tech-firm-to-breed-prawns](https://www.businesstimes.com.sg/companies-markets/oceanus-invests-in-deep-tech-firm-to-breed-prawns)\n\n2. Signed an agreement with Hainan Raffles Group, to set up the world's first Oceanus FoodTech Hub in Hainan. A key aquaculture center for shrimp and fish farming in the region.\n\nLink: [https://links.sgx.com/1.0.0/corporate-announcements/Q98FNYLCZ2E1YRFB/669685e053e41e000255387677e65a2f6919e620ef5c6b240ce4eb1a489ba10d?fbclid=IwAR38wSvIJMLFq\\_KUBYI0nmhTuNodYfg22ztw-z58JpcVCDyLA6ibWb-OYGM](https://links.sgx.com/1.0.0/corporate-announcements/Q98FNYLCZ2E1YRFB/669685e053e41e000255387677e65a2f6919e620ef5c6b240ce4eb1a489ba10d?fbclid=IwAR38wSvIJMLFq_KUBYI0nmhTuNodYfg22ztw-z58JpcVCDyLA6ibWb-OYGM)\n\n&#x200B;\n\n***Upcoming Near-term key Catalyst***  \n\n\n1. **Q4 2020 Results**. The Q4 2020 results will be released this coming February and in my opinion, it will no doubt be great as compared to the previous quarter.\n\n&#x200B;\n\n2. **Exiting from SGX watch-list**. Based on the profitability achieved in Q1-Q3 2020, Oceanus is on track to fulfill the condition to exit from SGX watch-list. This is an upgrade of confidence from SGX as it is loosening its reporting requirement for Oceanus.\n\n&#x200B;\n\n3. **Exponential revenue and earnings growth from Season Global**. Since establishing Season Global JV in Jan 2020, the revenue of Oceanus Group has grown significantly. In Q1-Q3 2020, Oceanus Group's revenue grew by 626% year over year ( +276% quarter over quarter ) and made a turnaround from a loss to profit. \n\n&#x200B;\n\n4. **Further expansion of aquaculture businesses**. The Covid-19 pandemic has accelerated the demand for many major cities to build their own food supplies. The could open up more opportunities for Oceanus to deploy its food tech hubs in key cities across China, ASEAN, and the Middle East.\n\n&#x200B;\n\n***Bearish Opinion***\n\nOf course, there will definitely be some bearish opinions as there is bullish.  \n\n\n1. Oceanus Group's valuation is a whopping $1.822 billion as of this writing. Its share price is at $0.075 on 19/02/2020 closing.   \n\n\n2. Oceanus Group's P/B ratio is at 76.27x as compared to its fair value and price relative to the market.\n\nLink: [https://www.theedgesingapore.com/capital/right-timing/caution-warranted-penny-stocks-overbought-highs-sti-slumps](https://www.theedgesingapore.com/capital/right-timing/caution-warranted-penny-stocks-overbought-highs-sti-slumps)  \n\n\nBased on the above numbers, Oceanus Group is overvalued as compared to other counters such as First Resources Ltd, Bumitama Agri Ltd, and Indofood Agri Resources Ltd to name a few. However, I would not use these numbers to value Oceanus Group as it is a growth company. We invest based on how we see the company's future, and from how I see it, Oceanus Group is en route to greater growth and earnings with strong fundamentals that are built since 2014.\n\n&#x200B;\n\n***Other Links***  \n\n\nTo those who would love to know more about Oceanus Group or where I get my research from, below are a few links provided for your convenience.  \n\n\n**UOB KayHian Analyst Report on Oceanus Group**\n\nLink: [https://research.sginvestors.io/2021/01/oceanus-group-uob-kay-hian-research-2021-01-20.html](https://research.sginvestors.io/2021/01/oceanus-group-uob-kay-hian-research-2021-01-20.html)  \n\n\n**89.3 Money FM interview on Oceanus Group CEO Peter Koh**\n\nLink: [https://omny.fm/shows/money-fm-893/driving-a-resilient-aquaculture-business-amid-covi?fbclid=IwAR2YoxNBFyWbjDwkaVmAeCBDYYLvRP40hC5KttwRnBWPhgJd5IMSrSxYvQA#description](https://omny.fm/shows/money-fm-893/driving-a-resilient-aquaculture-business-amid-covi?fbclid=IwAR2YoxNBFyWbjDwkaVmAeCBDYYLvRP40hC5KttwRnBWPhgJd5IMSrSxYvQA#description)  \n\n\n**Oceanus Facebook (Oceanus post updates on their progress)**\n\nLink: [https://www.facebook.com/OceanusGroupLimited](https://www.facebook.com/OceanusGroupLimited)\n\n&#x200B;\n\n**Disclaimer**: All content on this post is for informational & educational purposes only, and shouldn't be taken as personalized financial advice. Always do your own due diligence before investing. Cheers!",
            "title":"Oceanus still Bullish",
            "score":9,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lo3o1x/oceanus_still_bullish/"
        },
        {
            "datetime_created":"2021-02-09 11:11:58",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"jerrickng",
            "text":"Profit off Human Vanity. The vanity of human wishes.  \nInMode offers cutting edge medical devices for minimally-invasive & non-invasive procedures  \n\n\nInMode (INMD)  \nTonight they will announce the next financial release, based on 3Q 2020 we have:  \n\n\nIncome Growth:  \n\\+49% revenue growth Y/Y (3Q 2020 vs 3Q 2019), and that is during covid. Expecting a much stronger growth after vaccine roll out this year.  \nVery Profitable:  \nHigh Gross margin of 87.06% and Profit margin of 39.11% and ROE of 28.56%  \nIndustry Backdrop:  \nConstant year on year growth in demand for medical aesthetics procedures globally. It has just entered China market.   \n\n\nMy previous records (You can search my threads created)  \nSilvergate (Bought at $74, now $143) Gain +93.2%\n\nLets go onboard the next starship guys!\n\n&#x200B;\n\nhttps://preview.redd.it/o3gibm0rcdg61.jpg?width=589&format=pjpg&auto=webp&s=f8ed467d375007c467606cec8bde35c72f397b0e",
            "title":"InMode - Profit off Human Vanity",
            "score":3,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lft87s/inmode_profit_off_human_vanity/"
        },
        {
            "datetime_created":"2021-02-07 14:04:29",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"oceanus-medtecs",
            "text":"Open to the $The Place Hldg(E27.SI) sort of rise or the $Oceanus\\^(579.SI) sort of steady rise. Or even $Jiutian Chemical(C8R.SI) Please give names with Good Reasons. SGX focus for now though Im considering the likes of $PLTR . \n\nPlease give good ones, micro pennies with bad track record and repute not really welcome unless the team is reputable and non-China random folks like $OEL(584.SI) and please no $Medtecs Intl(546.SI) or $Sri Trang Agro(NC2.SI) those max 1.5x-2x from current levels. \n\nIn exchange, if selected, will share my own DUE D, if buy, will HYPE train it. And if really MB and I bought, can give u reward: 10 Teh Bings.\n\nMB preference: MIN 3x to 50X. Prefer 10-Bagger!",
            "title":"[Multi-Baggers: Probably a BAD Place to Source for MBs but in need of inspiration and lazy to do the 1st leg of work]",
            "score":6,
            "url":"https://www.reddit.com/r/Sgxbets/comments/legs37/multibaggers_probably_a_bad_place_to_source_for/"
        },
        {
            "datetime_created":"2021-02-04 23:47:15",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"oceanus-medtecs",
            "text":"$Oceanus\\^(579.SI) greg\\_dfvalue EVEN MALAY eat Abalone? Dubai, Middle East! Trade Oil for Abalones? HUAT LA. FINAL DUE D by greg\\_dfvalue!  \n\n\n>I think people will eat more abalone in the future.\n\nYONG HUI: Is abalone consumption growing?\n\n  \nPETER: Yes, I think people will eat more abalone in the future. A lot of restaurants and weddings are now shying away from shark's fins due to environmental reasons. This helps increase the demand for abalone.\\xa0Recently, many are also using abalone in yusheng instead of raw fish. Petrol kiosks also ran out of abalone during the Chinese New Year period.\n\n  \nYONG HUI: What is your retail strategy? Are you competing on price?\n\n  \nPETER: I don’t want to fight on price, because if we fight a price war, the company will not survive. We will price it in a way which is value for money, with the focus on quality, rather than being cheap or expensive. Generally, abalone isn’t cheap as people know. Anyone who buys abalone does not mind paying a few more dollars. They go for the quality and taste. We also want our abalones\\xa0to be\\xa0halal-certified.\n\n  \nYONG HUI: Are non-Chinese eating abalone?\n\n  \nPETER: It is still a small number now, but it will grow with education. Some try out\\xa0of curiosity. Why do the Chinese like it so much? It is slowly opening up, and this will give us a larger market.\n\n  \nYONG HUI: Is Indonesia one of the markets you want to educate?\n\n  \nPETER: We are looking to enter the whole of Asia-Pacific.\n\n  \nYONG HUI: Where can people expect to find your abalone?  \nPETER: We will start with e-commerce because we are not large-scale enough for the traditional channels—neither do we have the retail operations or the SKUs for that, so we will tie up with ecommerce partners, as well as through our own ecommerce channel.\n\n  \nMORALITY ETHICS CHECK\n\n  \nYONG HUI: How do you ensure the quality of your abalone?  \nPETER: For example, even though we have to pay two or three times more to ship our abalones to Australia to process it there, we do it. We have been approached by very questionable vendors in China who promised us many things. They say they can “value-add” at no extra cost, to make the abalones look bigger and whiter. The only condition is not to\\xa0ask how they do it! We are not comfortable with such things.\n\n  \nPOWER INDON BIZ  \nYONG HUI: Will your canned abalones be branded Oceanus?  \nPETER: Yes, and that explains why we are so careful about this, because we are literally\\xa0putting the company's name on the product.  \nYONG HUI: What has been the response so far?  \nPETER: There was this Indonesia couple whom I know through a friend—they wanted to throw a feast and wanted to buy some abalone, so we sent them a few cans. They got back, with an order for ten cartons. We are not the cheapest, but yet they chose our abalones. She brought me into their kitchen and showed me a whole row of other brands they had tried. She asked why our abalones aren’t bigger. . . so I explained to her.\n\n  \nHOW NOT TO INVEST IN OCEANUS AND THIS MAN \\[Read on\\]\n\n  \nPETER: What shareholders should do is believe in themselves. After seeing what we as a company is doing to change, they have to decide. In the past, there was a lot of talk,\\xa0but nothing happened. Right now, they have to see for themselves whether we have changed, and did we see things through and deliver our plans.\\xa0During our last AGM, there were a lot of questions from disgruntled shareholders, but\\xa0what started off as\\xa0a rowdy crowd, at\\xa0the end, they understood better\\xa0where\\xa0Oceanus is heading. What took me by surprise was this middle-aged lady who shouted: Mister CEO, now that you have said all these, should I buy more shares? \\[*laughs*\\] That was\\xa0a very difficult question. Look, I cannot control the market. I can tell you what the direction of the company is, but I cannot tell you how to invest your money.\\xa0Interestingly enough,\\xa0this other gentleman who was quite vocal shouted back—what are you waiting for? Go and buy!\n\n  \nYONG HUI: Will you consider taking the company private?\n\n  \nPETER: We don't have that in mind.\n\n  \nYONG HUI: Might that be beneficial for the company?\n\n  \nPETER: It won’t be beneficial to the shareholders. When you do that, it is over for the shareholders who bought earlier. It isn’t doing them a service.\\xa0My moral obligation is to do well for our shareholders and employees. I have to be accountable to shareholders.\n\n  \nhttps://www.hnworth.com/article/become/high-profiles/peter-koh-ceo-oceanus-group-limited/",
            "title":"Oceanus: 2016 CEO Interview",
            "score":6,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lcihr3/oceanus_2016_ceo_interview/"
        },
        {
            "datetime_created":"2021-02-04 12:32:58",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"oceanus-medtecs",
            "text":"I am going to start with the Concerns\n\n1. Valuation/Market Cap given run-up in share price\n\nThe concern really is Oceanus worth 1.5-2 Billion esp since many have done, it would be hard for Results to justify their PE ratio. Valid Concern, though read below. \n\n2. More Naysayers + Shortists which also means more Contra Buyers (i.e Speculation + Smart Alecs)\n\n70 Million Shorts YTD + More At Forum shouting down: The issue is we are NOT sure if Oceanus BB want to support, Long Retails have Limited Funds. Valid concern, if cannot hold, perhaps Sell? If got bullets, must have Strategy to Fight! 1st Half of the Day: Avoid the Battle. 2nd Half is where the Daily Battle Starts. If possible Try 4.38PM and each buy up as much as u can. then leave half to park at the price you buy. Say we manage to buy up 6.3. Then Block 6.3, force the shorts to cover 6.4 and beyond. If ONE day we strong enough, we play better block 6.3 and queue 6.5, make the shorts lose 2 pips. LAGI best is alot of Shorts queue say 6.6. End of the Day, we BUY up, force Naked Shorts, next day SGX BUY-IN + Make them Pay 1k SGD per day!\n\nWhat are the Good Catalysts? \n\n1. Macro Factors: Stimulus of US (Hot Money/Flush of Cash)\n\nBiden stimulus is more or less. Will this be good for the market? Yes liquidity, hot money.\n\n2. Impending Results: What to Look out For\n\nDon't expect results to be SO SO good to justify the current price. See the results in this Context:\n\nA. Results Backward Looking: It is Pandemic Results, if good = great, cause pandemic got good means no pandemic = great.\n\nB. Cyclical: Q1 which is NOW, is NOT reflected in the coming results, meaning this is a ADDED boost.\n\nLook out for\n\nC. Increase in Revenue/Profit %\n\nD. Are the results in line with EXITing SGX watchlist\n\nE. Forward Looking Statements\n\nF. Breakdown of Revenue as well as COSG\n\n3. SGX Watchlist: Inevitable, Signs are There (MAJOR FACTOR)\n\nCOMPANY Already HINT liao. PAP Top Star Join liao. Also Once Exit Watch List means BB can ENTER. Temasek, Ark Invest will ENTER Deep Tech + 2030 Food Security\n\n4. Rumours of Oceanus Abalone in PAP goodie bag to citizen \n\nIf true, Ah Kong support. See SIA: Ah kong have UNLIMITED MONEY and RULES to Favour who they want to save. \n\n5. Misunderstood Abalone Play + Misunderstood China Lockdown and No Abalone Eating \n\nSome claim China Lockdown and No Abalone Eating. That someone is a Boomer who reads Google headlines. I am in China, CNY in full Swing and ABALONE is a BIG THING. Please don't be a Boomer or Ostrich. \n\nNOT a Call to Buy because Price Up alot liao + Alot of Shortist lurking. if want to buy, must diamond hands.",
            "title":"$Oceanus^(579.SI) [Analysis: Both Sides]",
            "score":8,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lc7kcd/oceanus579si_analysis_both_sides/"
        },
        {
            "datetime_created":"2021-02-03 22:47:29",
            "source":"Reddit",
            "ticker":[
                "China"
            ],
            "publisher":"johnwickjj001",
            "text":"**Listen here retards, this DD is gold**  \n\nJT is ready to 🌚 \n \nASP of its products are 🚀🚀🚀  \n\nDMA price surged to 14k/ton[http://www.100ppi.com/mprice/?f=search&c=product&terms=%E4%BA%8C%E7%94%B2%E5%9F%BA%E4%B9%99%E9%85%B0%E8%83%BA](http://www.100ppi.com/mprice/?f=search&c=product&terms=%E4%BA%8C%E7%94%B2%E5%9F%BA%E4%B9%99%E9%85%B0%E8%83%BA)\n\nDMF price 10k/ton[http://www.100ppi.com/mprice/?f=search&c=product&terms=DMF](http://www.100ppi.com/mprice/?f=search&c=product&terms=DMF)\n\nUOBKH DMF asp assumption 7k/ton, CIMB 6k/ton... Whuuuuttttt?!?!  \nThis stock is fucking cheap, trading at 3x PE? WTF... vs China peers, Hualu Hengsheng 40x PE... and Hualu share price hit ATH.   \n💎💎💎🙌🙌🙌",
            "title":"Jiutian - push up to 九重天",
            "score":3,
            "url":"https://www.reddit.com/r/Sgxbets/comments/lbp2rg/jiutian_push_up_to_九重天/"
        },
        {
            "datetime_created":"2021-02-01 13:47:10",
            "source":"Reddit",
            "ticker":[
                
            ],
            "publisher":"Gn-85",
            "text":"Asian market going up",
            "title":"I realised that today Asian stock market don’t go down purposely due to US H-fund make it huge selling in Asian stock market... they will also be failed ...I think China government shall be taken action for that.",
            "score":1,
            "url":"https://www.reddit.com/r/Sgxbets/comments/l9w3tr/i_realised_that_today_asian_stock_market_dont_go/"
        }
    ]
    #DB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["is3107db"]
    mycol = mydb["reddit"]
    mycol.insert_many(sgx_list)

