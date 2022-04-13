import pymongo
import vanity
import pandas as pd
import json
from datetime import datetime, timedelta

def get_stocknews_data():
    tickers_dict = {
        'DBSDY':'DBS Group Holdings Ltd',
        'UOVEY': 'United Overseas Bank Limited',
        'SINGY': 'Singapore Airlines Limited',
        'SE': 'Sea Limited',
        'FXSG': 'Invesco CurrencyShares Singapore Dollar',
        'EWS':  'iShares MSCI Singapore Capped ETF',
        'MTGCF': 'Mapletree North Asia Commercial Trust',
        'STX': 'Seagate Technology plc',
        'FUTU': 'Futu Holdings Limited',
        'ACDSF': 'Ascendas Real Estate Investment Trust',
        'CLLDY': 'CapitaLand Integrated Commercial Trust'
    }
   
    doc = vanity.get_jsonparsed_data("https://stocknewsapi.com/api/v1?tickers=DBSDY,UOVEY,SINGY,SE,FXSG,EWS,MTGCF,STX,FUTU,ACDSF,CLLDY&items=50&token=cdxgrhebia7lvobqdvhfbhhk0wahvwlyo2e9kkmj")['data']

    # if API expires, use mock data
    # doc = [{
    #     "news_url": "https://www.fool.com/investing/2022/04/13/3-high-yielding-dividend-stocks-to-buy-on-the-dip/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6741572fa-person-smiling-and-reviewing-their-financesjpgw700opresize-1319068.jpg",
    #     "title": "3 High-Yielding Dividend Stocks to Buy on the Dip",
    #     "text": "These stocks look like some of the best bargains out there right now.",
    #     "source_name": "The Motley Fool",
    #     "date": "Wed, 13 Apr 2022 10:30:00 -0400",
    #     "topics": [
    #         "dividend"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "BIG",
    #         "PFE",
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/04/4-great-global-stocks-to-diversify-your-portfolio/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/2/l/oil13-1318556.jpg",
    #     "title": "4 Great Global Stocks to Diversify Your Portfolio",
    #     "text": "These global stocks are worth adding to your portfolio with a possibility of international markets outperforming U.S. markets. The post 4 Great Global Stocks to Diversify Your Portfolio appeared first on InvestorPlace.",
    #     "source_name": "InvestorPlace",
    #     "date": "Wed, 13 Apr 2022 07:53:40 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "EQNR",
    #         "RADA",
    #         "SE",
    #         "XPEV"
    #     ]
    # },
    # {
    #     "news_url": "https://seekingalpha.com/article/4501139-ews-etf-still-solid",
    #     "image_url": "https://cdn.snapi.dev/images/v1/l/4/image-1353756939-1318389.jpg",
    #     "title": "EWS: Still Solid As A Rock",
    #     "text": "BlackRock's iShares MSCI Singapore ETF holds a small portfolio of mostly blue chip companies. As with all market weighted ETFs, it will include companies which are neither profitable nor attractive in my opinion.",
    #     "source_name": "Seeking Alpha",
    #     "date": "Wed, 13 Apr 2022 06:50:11 -0400",
    #     "topics": [
    #         "paylimitwall"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "EWS"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/04/7-blue-chip-stocks-at-all-time-low-rkt-path-se-bidu-ccl-luv-gm/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/s/o/data-internet19-1318366.jpg",
    #     "title": "7 Blue-Chips Stocks to Buy at All-Time Lows",
    #     "text": "While the concept of buying discounts is appealing, prospective investors should specifically focus on deflated blue-chip stocks. The post 7 Blue-Chips Stocks to Buy at All-Time Lows appeared first on InvestorPlace.",
    #     "source_name": "InvestorPlace",
    #     "date": "Wed, 13 Apr 2022 06:30:07 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "BIDU",
    #         "CCL",
    #         "GM",
    #         "LUV",
    #         "PATH",
    #         "RKT",
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/12/3-high-yield-tech-stocks-to-buy-in-april/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6383342fmature-person-works-on-a-laptop-at-homejpgw700opresize-963899-988301-1317446.jpg",
    #     "title": "3 High-Yield Tech Stocks to Buy in April",
    #     "text": "Seagate, Qualcomm, and Broadcom are all solid income stocks.",
    #     "source_name": "The Motley Fool",
    #     "date": "Tue, 12 Apr 2022 11:45:00 -0400",
    #     "topics": [
    #         "dividend"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "AVGO",
    #         "QCOM",
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/12/better-buy-seagate-technology-vs-western-digital/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/t/h/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6742162fgettyimages-692220406jpgw700opresize-1316511.jpg",
    #     "title": "Better Buy: Seagate Technology vs. Western Digital",
    #     "text": "Which data storage stock is the better long-term investment?",
    #     "source_name": "The Motley Fool",
    #     "date": "Tue, 12 Apr 2022 06:56:00 -0400",
    #     "topics": [],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "STX",
    #         "WDC"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/11/why-sea-limited-floated-above-the-market-on-monday/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/i/4/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6743362fgettyimages-1217580202jpgw700opresize-1316230.jpg",
    #     "title": "Why Sea Limited Floated Above the Market on Monday",
    #     "text": "An analyst at a prominent investment bank gives the thumbs-up to the company's shares.",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 11 Apr 2022 18:39:09 -0400",
    #     "topics": [],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.gurufocus.com/news/1682886/top-3-ecommerce-stocks-with-a-huge-growth-runway",
    #     "image_url": "https://cdn.snapi.dev/images/v1/w/f/catalog-mail10-1315426.jpg",
    #     "title": "Top 3 E-Commerce Stocks With a Huge Growth Runway",
    #     "text": "Global e-commerce, already on a high-growth path, saw sales growth accelerate faster than expected in 2020 due to the pandemic, jumping by 25.7% according to data from eMarketer. As of 2022, around 21% of all retail sales are completed online, and this is expected to increase to 24.5% by 2025.",
    #     "source_name": "GuruFocus",
    #     "date": "Mon, 11 Apr 2022 11:45:05 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "BABA",
    #         "MELI",
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/09/sea-limited-stock-could-resurge-after-its-recent-s/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/p/o/podc8-1314118.jpg",
    #     "title": "Sea Limited Stock Could Resurge After Its Recent Slide",
    #     "text": "Is a comeback on the horizon for this stock?",
    #     "source_name": "The Motley Fool",
    #     "date": "Sat, 09 Apr 2022 08:00:00 -0400",
    #     "topics": [
    #         "podcast"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://stockmarket.com/featured/4-top-computer-hardware-stocks-to-watch-right-now-2022-04-07",
    #     "image_url": "https://cdn.snapi.dev/images/v1/l/k/computer-hardware-stocks-1024x576-1312466.jpg",
    #     "title": "4 Top Computer Hardware Stocks To Watch Right Now",
    #     "text": "Investors could be turning their attention to computer hardware stocks.",
    #     "source_name": "Stockmarketcom",
    #     "date": "Thu, 07 Apr 2022 17:00:59 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "DELL",
    #         "HPQ",
    #         "LNVGY",
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://www.zacks.com/stock/news/1894880/seagate-stx-phison-collaborate-to-advance-ssd-development",
    #     "image_url": "https://cdn.snapi.dev/images/v1/y/l/data-internet26-1311955.jpg",
    #     "title": "Seagate (STX) & Phison Collaborate to Advance SSD Development",
    #     "text": "Seagate Technology Holdings plc (STX) is teaming up with Phison Electronics Corp to augment SSD technology development.",
    #     "source_name": "Zacks Investment Research",
    #     "date": "Thu, 07 Apr 2022 12:48:18 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/04/3-beaten-down-stocks-to-buy-for-tactical-rebound-rallies/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/m/r/bank6-1311778.jpg",
    #     "title": "3 Beaten Down Stocks to Buy For Tactical Rebound Rallies",
    #     "text": "The red days this week are not necessarily the beginning of the end. Here are 3 stocks to buy after months of trepidation.",
    #     "source_name": "InvestorPlace",
    #     "date": "Thu, 07 Apr 2022 11:24:26 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "C",
    #         "HD",
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/07/have-1000-these-stocks-could-be-bargain-buys-2022/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6734332fperson-unpacking-a-boxjpgw700opresize-1311090.jpg",
    #     "title": "Have $1,000? These 2 Stocks Could Be Bargain Buys for 2022 and Beyond",
    #     "text": "These two stocks could be great ways to take advantage of the market downturn.",
    #     "source_name": "The Motley Fool",
    #     "date": "Thu, 07 Apr 2022 07:40:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "MELI",
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/04/se-stock-sea-limited-has-a-long-runway-ahead-of-it/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/j/o/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f5795682fasian-smartphone-online-gaming-video-sea-limited-gettyjpegw700opresize-1202275-1309771.jpg",
    #     "title": "Sea Limited Stock Has a Long Runway Ahead of It",
    #     "text": "From deep corrections come strong rebound rallies. SE stock is coming back from the abyss, so it has miles of runway ahead of it this year.",
    #     "source_name": "InvestorPlace",
    #     "date": "Wed, 06 Apr 2022 10:54:52 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.businesswire.com/news/home/20220406005118/en/Seagate-and-Phison-Broaden-Partnership-to-Bolster-Portfolio-of-High-Performance-High-Density-Enterprise-Class-Solid-State-Drives-Optimized-to-Lower-Data-Center-TCO/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/3/f/press15-1309263.jpg",
    #     "title": "Seagate and Phison Broaden Partnership to Bolster Portfolio of High-Performance, High-Density Enterprise-Class Solid State Drives Optimized to Lower Data Center TCO",
    #     "text": "FREMONT, Calif.--(BUSINESS WIRE)--Seagate\u00ae Technology Holdings plc (NASDAQ: STX), a world leader in mass-data storage infrastructure solutions, and Phison Electronics Corp. (TPEX: 8299), a global leader in NAND flash controller and storage solutions, announced today plans to expand their SSD portfolio of next-gen high-performance, high-density enterprise NVMe SSDs. The new SSDs will help enterprises lower total cost ownership (TCO) through increased storage density, lower power consumption, and",
    #     "source_name": "Business Wire",
    #     "date": "Wed, 06 Apr 2022 08:00:00 -0400",
    #     "topics": [
    #         "PressRelease"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/05/my-take-4-strong-growth-stocks-to-buy-this-week/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6731752fgettyimages-1297492947jpgw700opresize-1307078.jpg",
    #     "title": "My Take: 4 Strong Growth Stocks To Buy This Week",
    #     "text": "These ad tech, e-commerce, gaming, and cybersecurity stocks deserve to go higher.",
    #     "source_name": "The Motley Fool",
    #     "date": "Tue, 05 Apr 2022 07:20:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "BZUN",
    #         "FTNT",
    #         "SE",
    #         "TTD"
    #     ]
    # },
    # {
    #     "news_url": "https://seekingalpha.com/article/4499769-sea-stock-shopee-moving-out-india-good-bad",
    #     "image_url": "https://cdn.snapi.dev/images/v1/d/b/software38-1306766.jpg",
    #     "title": "Sea Limited's Shopee Moving Out Of India: Good Or Bad?",
    #     "text": "Last week, Sea Limited announced that Shopee would withdraw from India.",
    #     "source_name": "Seeking Alpha",
    #     "date": "Mon, 04 Apr 2022 23:24:33 -0400",
    #     "topics": [
    #         "paylimitwall"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/04/why-sea-limited-stock-jumped-today/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/w/1/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6733272fgettyimages-1177802719jpgw700opresize-1306290.jpg",
    #     "title": "Why Sea Limited Stock Jumped Today",
    #     "text": "Investors are getting more optimistic about Chinese tech stocks.",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 04 Apr 2022 14:19:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/04/why-shares-of-ke-holdings-futu-and-up-fintech-are/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/a/i/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6732742fgeneric-upward-5-gettyjpgw700opresize-1306058.jpg",
    #     "title": "Why Shares of KE Holdings, Futu, and UP Fintech Are Rising Today",
    #     "text": "U.S. and Chinese financial regulators appear to be making more progress on their auditing dispute.",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 04 Apr 2022 12:33:01 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "BEKE",
    #         "TIGR",
    #         "FUTU"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/03/dont-let-this-1-decision-sour-you-on-sea-limited/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/h/c/software42-1304681.jpg",
    #     "title": "Don't Let This 1 Decision Sour You on Sea Limited",
    #     "text": "Robust execution and a large market opportunity position Sea for long-term success.",
    #     "source_name": "The Motley Fool",
    #     "date": "Sun, 03 Apr 2022 08:36:00 -0400",
    #     "topics": [],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/02/why-sea-limited-declined-by-177-in-march/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/z/9/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6731702fgirl-gaming-on-desktopjpgw700opresize-1304588.jpg",
    #     "title": "Why Sea Limited Declined by 17.7% in March",
    #     "text": "The e-commerce company reported its very first quarter-over-quarter fall in users for its gaming division.",
    #     "source_name": "The Motley Fool",
    #     "date": "Sat, 02 Apr 2022 22:30:00 -0400",
    #     "topics": [],
    #     "sentiment": "Negative",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/02/3-things-every-sea-limited-investor-must-know/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6727272fperson-shopping-online-looking-at-his-phonejpgw700opresize-1304515.jpg",
    #     "title": "3 Things Every Sea Limited Investor Must Know",
    #     "text": "News has been flying about Sea Limited, but investors should remain optimistic.",
    #     "source_name": "The Motley Fool",
    #     "date": "Sat, 02 Apr 2022 11:30:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/01/why-shares-of-alibaba-didi-global-and-futu-are-ris/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/g/i/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6729712fgeneric-upward-stock-move-gettyjpgw700opresize-1303796.jpg",
    #     "title": "Why Shares of Alibaba, DiDi Global, and Futu Are Rising",
    #     "text": "Some good news came out today regarding the ongoing auditing dispute between U.S. and Chinese financial regulators.",
    #     "source_name": "The Motley Fool",
    #     "date": "Fri, 01 Apr 2022 13:01:13 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "BABA",
    #         "DIDI",
    #         "FUTU"
    #     ]
    # },
    # {
    #     "news_url": "https://www.prnewswire.com/news-releases/offering-investors-a-16-hour-trading-window-moomoo-achieves-record-user-number-301515925.html",
    #     "image_url": "https://cdn.snapi.dev/images/v1/p/r/press5-1303797.jpg",
    #     "title": "Offering Investors a 16-hour Trading Window, Moomoo Achieves Record User Number",
    #     "text": "PALO ALTO, Calif., April 1, 2022 /PRNewswire/ -- Moomoo, the next-generation one-stop digital financial service platform, announced that it had accumulated over 18 million users from more than 200 countries and regions with its sister brand.",
    #     "source_name": "PRNewsWire",
    #     "date": "Fri, 01 Apr 2022 12:53:00 -0400",
    #     "topics": [
    #         "PressRelease"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "FUTU"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/04/a-3-billion-fund-just-bought-futu-stock-heres-why/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/w/asset-management8-1303608.jpg",
    #     "title": "A $3 Billion Fund Just Bought FUTU Stock. Here's Why.",
    #     "text": "Shares of FUTU stock are in the green this morning after China announced a positive development towards complying with U.S. audit regulations. The post A $3 Billion Fund Just Bought FUTU Stock.",
    #     "source_name": "InvestorPlace",
    #     "date": "Fri, 01 Apr 2022 11:11:56 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "FUTU"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/04/01/1-green-flag-for-sea-limited-in-2022-and-1-red-fla/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6725952fgettyimages-1130929699jpgw700opresize-1303518.jpg",
    #     "title": "1 Green Flag for Sea Limited in 2022, and 1 Red Flag",
    #     "text": "Sea remains a polarizing stock for the bulls and the bears.",
    #     "source_name": "The Motley Fool",
    #     "date": "Fri, 01 Apr 2022 10:30:00 -0400",
    #     "topics": [],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.gurufocus.com/news/1675141/sea-limited-a-growth-monster-at-a-reasonable-price",
    #     "image_url": "https://cdn.snapi.dev/images/v1/f/d/fde2-1301741.",
    #     "title": "Sea Limited: A Growth Monster at a Reasonable Price",
    #     "text": "Sea is a leading consumer internet company based in Southeast Asia",
    #     "source_name": "GuruFocus",
    #     "date": "Thu, 31 Mar 2022 11:58:05 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.gurufocus.com/news/1675141/sea-ltd-a-growth-monster-at-a-reasonable-price",
    #     "image_url": "https://cdn.snapi.dev/images/v1/d/t/software16-1302094.jpg",
    #     "title": "Sea Ltd.: A Growth Monster at a Reasonable Price",
    #     "text": "Introduction",
    #     "source_name": "GuruFocus",
    #     "date": "Thu, 31 Mar 2022 11:58:05 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/03/why-is-futu-holdings-futu-stock-down-today/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/h/4/asset-management33-dhxhb1omqx-1301716.jpg",
    #     "title": "Why Is Futu Holdings (FUTU) Stock Down Today?",
    #     "text": "Shares of FUTU stock are in the red after the brokerage company was added to the HFCAA's list of companies in possible violation. The post Why Is Futu Holdings (FUTU) Stock Down Today?",
    #     "source_name": "InvestorPlace",
    #     "date": "Thu, 31 Mar 2022 11:33:09 -0400",
    #     "topics": [],
    #     "sentiment": "Negative",
    #     "type": "Article",
    #     "tickers": [
    #         "FUTU"
    #     ]
    # },
    # {
    #     "news_url": "https://www.businesswire.com/news/home/20220331005430/en/Seagate-Wins-Manufacturing-Leadership-Award-from-a-Jury-of-Its-Peers/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/f/u/press3-1301618.jpg",
    #     "title": "Seagate Wins Manufacturing Leadership Award from a Jury of Its Peers",
    #     "text": "FREMONT, Calif.--(BUSINESS WIRE)--Seagate Technology likes to keep its factories smart. Today, the company received an award for an achievement in smart manufacturing from a group of its manufacturing peers\u2014a national association of manufacturers with 14,000 company members. Seagate Technology Holdings plc (NASDAQ: STX), a world leader in data storage solutions, won a 2022 Manufacturing Leadership Award for its outstanding innovation from the Manufacturing Leadership Council (MLC) at the Nation",
    #     "source_name": "Business Wire",
    #     "date": "Thu, 31 Mar 2022 11:00:00 -0400",
    #     "topics": [
    #         "PressRelease"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/03/se-stock-hold-sea-limited-stock-until-negative-headwinds-clear-up/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/o/w/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6612472fsmartphone-city-connectivityjpgw700opresize-1185195-1241131-1300494.jpg",
    #     "title": "Hold Sea Limited Stock Until Negative Headwinds Clear Up",
    #     "text": "Tencent sold Sea shares in 2022, then India banned its hottest mobile game, putting extreme pressure on its share price. The post Hold Sea Limited Stock Until Negative Headwinds Clear Up appeared first on InvestorPlace.",
    #     "source_name": "InvestorPlace",
    #     "date": "Wed, 30 Mar 2022 19:33:13 -0400",
    #     "topics": [],
    #     "sentiment": "Negative",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/29/why-sea-limited-stock-blasted-higher-tuesday/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/d/8/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6724842fyoung-gamer-in-a-darkened-room-wearing-a-headset-while-playing-video-games-on-a-computerjpgw700opresize-1298044.jpg",
    #     "title": "Why Sea Limited Stock Blasted Higher Tuesday",
    #     "text": "Wall Street is weighing in on the company's recent decision.",
    #     "source_name": "The Motley Fool",
    #     "date": "Tue, 29 Mar 2022 14:18:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://seekingalpha.com/article/4498368-sea-limited-stock-exiting-india-entering-profitability",
    #     "image_url": "https://cdn.snapi.dev/images/v1/k/k/software21-1297760.jpg",
    #     "title": "Sea Limited: Exiting India, Entering Profitability",
    #     "text": "Sea's Shopee exit from India is a positive as it demonstrates management's strong capital discipline and reduces regulatory uncertainty given the ban of Free Fire India.",
    #     "source_name": "Seeking Alpha",
    #     "date": "Tue, 29 Mar 2022 11:46:07 -0400",
    #     "topics": [
    #         "paylimitwall"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.zacks.com/stock/news/1888992/here-s-why-trend-investors-would-love-betting-on-dbs-group-holdings-ltd-dbsdy",
    #     "image_url": "https://cdn.snapi.dev/images/v1/r/k/bank6-1297575.jpg",
    #     "title": "Here's Why \"Trend\" Investors Would Love Betting on DBS Group Holdings Ltd (DBSDY)",
    #     "text": "If you are looking for stocks that are well positioned to maintain their recent uptrend, DBS Group Holdings Ltd (DBSDY) could be a great choice. It is one of the several stocks that passed through our \"Recent Price Strength\" screen.",
    #     "source_name": "Zacks Investment Research",
    #     "date": "Tue, 29 Mar 2022 10:32:33 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "DBSDY"
    #     ]
    # },
    # {
    #     "news_url": "https://seekingalpha.com/article/4498219-sea-limited-stock-5-years",
    #     "image_url": "https://cdn.snapi.dev/images/v1/x/y/software15-1297196.jpg",
    #     "title": "Where Will Sea Limited Stock Be In 5 Years?",
    #     "text": "After a broad-market rebound in the past two weeks, SE stock remains down by 48% YTD, though it is up six-fold since its IPO.",
    #     "source_name": "Seeking Alpha",
    #     "date": "Tue, 29 Mar 2022 08:30:00 -0400",
    #     "topics": [
    #         "paylimitwall"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/29/3-gaming-growth-stocks-72-195-upside-wall-street/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6720922fthree-smiling-friends-playing-mobile-games-and-celebratingjpgw700opresize-1297212.jpg",
    #     "title": "3 Gaming Growth Stocks With 72% to 195% Upside, Says Wall Street",
    #     "text": "The red-hot gaming industry is set to catch a boost with new technologies like the 5G network and the metaverse.",
    #     "source_name": "The Motley Fool",
    #     "date": "Tue, 29 Mar 2022 08:26:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE",
    #         "SKLZ",
    #         "U"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/28/why-sea-limited-inched-higher-today/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/r/0/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6723582fwoman-in-clothing-shop-with-tabletjpgw700opresize-1296554.jpg",
    #     "title": "Why Sea Limited Inched Higher Today",
    #     "text": "The company is pulling one of its key businesses from the Indian market.",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 28 Mar 2022 18:50:44 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/03/the-10-entertainment-stocks-to-buy-for-2022-and-beyond/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/7/i/computer-electronic38-1296528.jpg",
    #     "title": "The 10 Entertainment Stocks to Buy for 2022 and Beyond",
    #     "text": "Entertainment stocks have delivered underwhelming returns in 2022. Here are 10 that have a chance to rebound and deliver for investors.",
    #     "source_name": "InvestorPlace",
    #     "date": "Mon, 28 Mar 2022 18:00:48 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "AAPL",
    #         "AMZN",
    #         "BILI",
    #         "EA",
    #         "NERD",
    #         "NXST",
    #         "PARA",
    #         "PEJ",
    #         "SE",
    #         "SKLZ"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/28/is-beaten-down-sea-limited-stock-ready-to-rebound/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/p/o/podc6-1295588.jpg",
    #     "title": "Is Beaten-Down Sea Limited Stock Ready To Rebound 10x?",
    #     "text": "Can it still become the Amazon and PayPal of Southeast Asia?",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 28 Mar 2022 09:15:00 -0400",
    #     "topics": [
    #         "podcast"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/03/why-is-sea-limited-se-stock-in-the-spotlight-today/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/x/q/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6662102fgettyimages-1343372840jpgw700opresize-1234463-1295612.jpg",
    #     "title": "Why Is Sea Limited (SE) Stock in the Spotlight Today?",
    #     "text": "SE stock is in focus today as Sea Limited shared further evidence that its international expansion plans have hit roadblocks. The post Why Is Sea Limited (SE) Stock in the Spotlight Today?",
    #     "source_name": "InvestorPlace",
    #     "date": "Mon, 28 Mar 2022 08:42:41 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/25/these-are-5-of-the-fastest-growing-large-cap-stock/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6702152fgettyimages-623351254jpgw700opresize-1293337.jpg",
    #     "title": "These Are 5 of the Fastest-Growing Large-Cap Stocks on the Planet",
    #     "text": "These companies have the size for stability and the growth to produce significant gains for investors.",
    #     "source_name": "The Motley Fool",
    #     "date": "Fri, 25 Mar 2022 07:45:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "AMD",
    #         "DDOG",
    #         "SE",
    #         "SNOW",
    #         "TTD"
    #     ]
    # },
    # {
    #     "news_url": "https://www.forbes.com/sites/greatspeculations/2022/03/25/why-has-seagate-technology-stock-doubled-since-2018-despite-just-7-sales-growth/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/h/g/why-has-seagate-technology-stock-doubled-since-2018-despite-just-7-sales-growth-1293135.jpg",
    #     "title": "Why Has Seagate Technology Stock Doubled Since 2018 Despite Just 7% Sales Growth?",
    #     "text": "Seagate Technology stock price gained 137% from around $38 at 2018 end, to over $90 currently, primarily due to favorable changes in its P/S multiple. However, the company witnessed just a 7% rise in revenue over this period, but revenue per share has increased, helped by a 23% drop in the.",
    #     "source_name": "Forbes",
    #     "date": "Fri, 25 Mar 2022 05:30:02 -0400",
    #     "topics": [
    #         "paylimitwall"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "STX"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/03/7-death-cross-stocks-to-buy-when-others-are-selling/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/a/x/3de233-1146621-1230398-1288040.jpg",
    #     "title": "7 Death-Cross Stocks to Buy When Others Are Selling",
    #     "text": "While the ominous nature of the death cross spells doom, history suggests this could be an opportunity for stocks to buy. The post 7 Death-Cross Stocks to Buy When Others Are Selling appeared first on InvestorPlace.",
    #     "source_name": "InvestorPlace",
    #     "date": "Tue, 22 Mar 2022 09:46:20 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "DKNG",
    #         "EL",
    #         "INTU",
    #         "SE",
    #         "SHOP",
    #         "SHW",
    #         "TWLO"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/21/why-sea-limited-stock-crashed-by-7-monday/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/m/0/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6648252fstock-market-chart-crash-correction-buy-investment-planning-laptop-gettyjpgw700opresize-1222181-1286835.jpg",
    #     "title": "Why Sea Limited Stock Crashed by 7% Monday",
    #     "text": "HSBC still likes the stock -- but not as much as it used to.",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 21 Mar 2022 15:57:58 -0400",
    #     "topics": [],
    #     "sentiment": "Negative",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://stockmarket.com/featured/4-top-communication-services-stocks-to-watch-in-march-2022-2022-03-21",
    #     "image_url": "https://cdn.snapi.dev/images/v1/g/o/asset-management30-1286790.jpg",
    #     "title": "4 Top Communication Services Stocks To Watch In March 2022",
    #     "text": "Could there be hidden gems among these communication services stocks?",
    #     "source_name": "Stockmarketcom",
    #     "date": "Mon, 21 Mar 2022 15:17:00 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "OMC",
    #         "SE",
    #         "TMUS",
    #         "ZM"
    #     ]
    # },
    # {
    #     "news_url": "https://www.fool.com/investing/2022/03/21/3-stocks-down-50-or-more-that-wall-street-thinks-c/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/u/r/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f6702602fcouple-with-woman-showing-man-ipadjpgw700opresize-1285570.jpg",
    #     "title": "3 Stocks Down 50% or More That Wall Street Thinks Could Nearly Double",
    #     "text": "They're beaten down -- but perhaps for not too much longer.",
    #     "source_name": "The Motley Fool",
    #     "date": "Mon, 21 Mar 2022 05:55:00 -0400",
    #     "topics": [],
    #     "sentiment": "Negative",
    #     "type": "Article",
    #     "tickers": [
    #         "SE",
    #         "SOFI",
    #         "TXG"
    #     ]
    # },
    # {
    #     "news_url": "https://www.reuters.com/article/mnact-m-a-mct/singapore-reit-mapletree-commercial-trust-adds-cash-only-option-to-3-billion-merger-idUSKCN2LI03G",
    #     "image_url": "https://cdn.snapi.dev/images/v1/m/0/m02d20220321t2i1594872384w940fhfwllplsqrlynxnpei2k01x-1285422.jpg",
    #     "title": "Singapore REIT Mapletree Commercial Trust adds cash-only option to $3 billion merger",
    #     "text": "Mapletree North Asia Commercial Trust's unitholders will now have an option to receive consideration in cash from a proposed S$4.2 billion ($3.10 billion) merger with Mapletree Commercial Trust, the Temasek-linked Singapore real estate investment trusts said on Monday.",
    #     "source_name": "Reuters",
    #     "date": "Sun, 20 Mar 2022 21:58:00 -0400",
    #     "topics": [
    #         "manda",
    #         "Real Estate"
    #     ],
    #     "sentiment": "Neutral",
    #     "type": "Article",
    #     "tickers": [
    #         "MTGCF"
    #     ]
    # },
    # {
    #     "news_url": "https://investorplace.com/2022/03/solid-revenue-growth-wont-save-se-stock-as-net-losses-widen/",
    #     "image_url": "https://cdn.snapi.dev/images/v1/l/h/445r3-945776-1063972-1213435-1284778.jpg",
    #     "title": "Solid Revenue Growth Won't Save Sea Limited Stock as Net Losses Widen",
    #     "text": "SE stock has been trending lower in 2022 despite the solid revenue growth. Don't trust claims that Sea Limited is a bargain now.",
    #     "source_name": "InvestorPlace",
    #     "date": "Fri, 18 Mar 2022 14:55:24 -0400",
    #     "topics": [
    #         "earnings"
    #     ],
    #     "sentiment": "Negative",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://seekingalpha.com/article/4496480-sea-limited-the-three-headed-monster",
    #     "image_url": "https://cdn.snapi.dev/images/v1/o/j/software4-1284625.jpg",
    #     "title": "Sea Limited: The Three-Headed Monster",
    #     "text": "Garena, Sea's only profitable segment, serves as a lifeline for its other two segments, but Bookings are expected to fall sharply in FY2022.",
    #     "source_name": "Seeking Alpha",
    #     "date": "Fri, 18 Mar 2022 13:01:14 -0400",
    #     "topics": [
    #         "paylimitwall"
    #     ],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "SE"
    #     ]
    # },
    # {
    #     "news_url": "https://www.zacks.com/stock/news/1883995/seagate-stx-is-a-top-ranked-growth-stock-should-you-buy",
    #     "image_url": "https://cdn.snapi.dev/images/v1/w/5/data-internet3-1284380.jpg",
    #     "title": "Seagate (STX) is a Top-Ranked Growth Stock: Should You Buy?",
    #     "text": "Wondering how to pick strong, market-beating stocks for your investment portfolio? Look no further than the Zacks Style Scores.",
    #     "source_name": "Zacks Investment Research",
    #     "date": "Fri, 18 Mar 2022 11:17:20 -0400",
    #     "topics": [],
    #     "sentiment": "Positive",
    #     "type": "Article",
    #     "tickers": [
    #         "STX"
    #     ]
    # }]

    df = pd.json_normalize(doc)
    df['datetime_created'] = [pd.to_datetime(x).tz_convert('Asia/Singapore').strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(x) else pd.NaT for x in df['date']]

    df['date'] = [pd.to_datetime(x) if not pd.isna(x) else pd.NaT for x in df['datetime_created']]
    df = df[df['date'] == (datetime.today() - timedelta(days=1)).date()]
    df.rename(columns={'source_name':'publisher','news_url':'url','tickers':'ticker'}, inplace=True)
    df['source'] = 'stocknews'
    df['ticker'] = [[tickers_dict[x] for x in lst if x in tickers_dict] for lst in df['ticker']]
    df.drop(columns=['image_url','topics','type','date','sentiment'], inplace=True)

    data = df.to_json(orient='records', lines=True).split('\n')[:-1]
    data = [json.loads(x) for x in data]

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["textual_db"]
    mycol = mydb["stocknews"]

    if mycol.count_documents({}) != 0:
        # If database has other day's data, clear it
        mycol.delete_many({})

    mycol.insert_many(data)
