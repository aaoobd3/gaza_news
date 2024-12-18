from GoogleNews import GoogleNews

import time
import newspaper
import json
import requests
from tqdm import tqdm
import base64
from datetime import datetime
gn = GoogleNews('ar')
gn.search("gaza healthcare + gaza hospitals")
gn.set_period('10d')
news_list = []
for i in tqdm(range(1,4),"pages"):
  gn.get_page(i)
  news_list.extend(gn.get_links())

news_dict = {}
news_processed_list = []
for news in tqdm(news_list):
  
  try:
    article = newspaper.Article(url=news, language='ar')
    article.download()
    article.parse()

    article ={
        "link": news,
        "title": str(article.title),
        "text": str(article.text),
        "authors": article.authors,
        "published_date": str(article.publish_date),
        "top_image": str(article.top_image),
        "videos": article.movies,
        "keywords": article.keywords,
        "summary": str(article.summary)
    }
    news_processed_list.append(article)
  except:
    print("failed",news)
    pass
sorted_news_processed_list =  sorted(news_processed_list, key=lambda x: datetime.strptime(x["published_date"], "%Y-%m-%d %H:%M:%S") if x["published_date"] else datetime.min, reverse=True)

news_dict["news"] = sorted_news_processed_list

with open("news.json","w") as x:
   json.dump(news_dict,x)

  