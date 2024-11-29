from pygooglenews import GoogleNews
from googlenewsdecoder import new_decoderv1

import time
import newspaper
import json
import requests
from tqdm import tqdm
import base64
from datetime import datetime,timedelta
def decode(source_url):

    interval_time = 1 # default interval is 1 sec, if not specified


    try:
        decoded_url = new_decoderv1(source_url, interval=interval_time)
        if decoded_url.get("status"):
            print("Decoded URL:", decoded_url["decoded_url"])
            return decoded_url["decoded_url"]
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        pass



gn = GoogleNews(lang='ar',country='ME')

days_before = 200

# Generate 'to' and 'from' dates
to_date = datetime.now()
from_date = to_date - timedelta(days=days_before)
# Format dates as strings
to_date_str = to_date.strftime('%Y-%m-%d')
from_date_str = from_date.strftime('%Y-%m-%d')
print(to_date_str,from_date_str)
top  = gn.search("الوضع الصحي في غزه",when='after:' + from_date_str + ' before:' +to_date_str)
news_list = [i["link"] for i in top["entries"]]

  


news_dict = {}
news_processed_list = []
for news in tqdm(news_list):
  
  try:
    news  = decode(news)
    article = newspaper.Article(url=news, language='ar')
    article.download()
    article.parse()

    article ={
        "link": news,
        "title": str(article.title),
        "text": str(article.text),
        "authors": article.authors,
        "published_date": str(article.publish_date.date()) if article.publish_date else "None",
        "top_image": str(article.top_image),
        "videos": article.movies,
        "keywords": article.keywords,
        "summary": str(article.summary)
    }
    news_processed_list.append(article)
    
    print(article['published_date'])
  except:
    print("failed",news)
    pass

sorted_news_processed_list =  sorted(news_processed_list, key=lambda x: datetime.strptime(x["published_date"], "%Y-%m-%d") if x["published_date"]!='None' else datetime.min, reverse=True)

news_dict["news"] = sorted_news_processed_list

with open("news.json","w") as x:
   json.dump(news_dict,x)

  