from pygooglenews import GoogleNews
from googlenewsdecoder import new_decoderv1

import time
import newspaper
import json
import requests
from tqdm import tqdm
import base64

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
top  = gn.search("الوضع الصحي في غزه")
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
  
news_dict["news"] = news_processed_list

with open("news.json","w") as x:
   json.dump(news_dict,x)

  