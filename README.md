# US News Website Parser + Google News SERP Data Extract

1. The program parses blog.feedspot.com catalog and scrapes websites directory data and adds data into MongoDB. 
2. Then the program checks the response HTTP status code of each website and ads data into MongoDB.
3. Next, the program gets SERP data on each website by certain keyword (e.g. "ukraine", input in terminal) 
via [Value SERP API](https://www.valueserp.com/docs/search-api/searches/common). The program will send requests to API only for "'available': True" marked websites.
4. Finally, the program writes all scraped data into final MongoDB database (`db_name = news_websites`, `collection = websites_with_serp_data`) and makes JSON dump named `website_data.json` in the program folder.

## Installation:
1. Install Python (>3.8.x recommended). Don't forget to tick a PATH option in setup process.
2. Download and install MongoDB from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) for your system.
3. In terminal type: `pip install -r requirements.txt`
4. Run program. In terminal: `python main.py` or `python3 main.py`.
5. Follow instructions in terminal and wait.
