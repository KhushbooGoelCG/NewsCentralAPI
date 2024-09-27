import json
import keyword
from urllib import response
import requests
import pandas as pd
import http.client
import openai
import os

from flask import jsonify,request
from PythonFlaskAPI import app
from serpapi import google_search
from newsapi import NewsApiClient
from gtts import gTTS


@app.route('/allnews', methods=['GET'])
def newsscrap(): 
    conn = http.client.HTTPSConnection("api.hasdata.com")
    headers = {
        'x-api-key': "75017e4d-6c6f-45c5-9b11-37bf70813e79",
        'Content-Type': "application/json"
    }
    conn.request("GET", "/scrape/google/serp?q=india+news&location=India&lr=lang_hi&lr=lang_en&tbm=nws&deviceType=desktop&gl=in&hl=en", headers=headers)
    res = conn.getresponse()
    data = res.read()
    jsondata = json.loads(data.decode("utf-8"))
    return jsondata



@app.route('/filterNews', methods=['GET'])
def filterNews(): 
    #passing parameters to the API through querystring
    #/filterNews?q=cricket&l=india
    query = request.args.get('q')
    location = request.args.get('l')

    conn = http.client.HTTPSConnection("api.hasdata.com")
    headers = {
        'x-api-key': "75017e4d-6c6f-45c5-9b11-37bf70813e79",
        'Content-Type': "application/json"
    }
    createdUrl = "/scrape/google/serp?q=" + query + "&location=" + location + "&tbm=nws&deviceType=desktop"
    conn.request("GET", createdUrl, headers=headers)
    res = conn.getresponse()
    data = res.read()
    jsondata = json.loads(data.decode("utf-8"))
    return jsondata



@app.route('/openAIIntegration', methods=['GET'])
def openAIIntegration(): 
    openai.api_key = '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'
    question = "India broadens engagement with Bangladesh's interim government, focusing on  security, energy, and economic cooperation amid political..."
    question += "  100 words"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": "search news"
          },
          {
            "role": "user",
            "content": question
          }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

    processed = response["choices"][0]["message"]["content"]
    return processed
    #response.choices[0].message.content

    
@app.route('/bingnews', methods=['GET'])
def bingnews(): 
    question = "sports"
    #question += "  100 words"

    params = {
    "api_key": "29c70faeb047fd54b8eb83f55271ab1da4e08fb7d7f45557b7548fec8b71f31e",                   
     # https://serpapi.com/manage-api-key
    
     "q": question,                      # search query
     "engine": "bing_news",              # search engine
     "cc": "in",                         # country of the search
    #'first': 1,                         # pagination
    #'count': 10,                        # number of results per page
    #'qft': 'interval="7"'               # news for past 24 hours
       }

    search = google_search.GoogleSearch(params)         # data extraction on the SerpApi backend
    results = search.get_dict()         # JSON -> Python dict

    bing_news_results = []
    #page_limit = 5

    #page_count = 0

    #while 'error' not in results and page_count < page_limit:
    ## data extraction from current page will be here

    #params['first'] += params['count']
    #page_count += 1
    #results = search.get_dict()

    bing_news_results.extend(results.get('organic_results', []))
    # title = results['organic_results'][0]['title']
    # link = results['organic_results'][0]['link']
    # snippet = results['organic_results'][0]['snippet']
    # source = results['organic_results'][0]['source']
    # date = results['organic_results'][0]['date']
    # thumbnail= results['organic_results'][0]['thumbnail']

    response = json.dumps(bing_news_results, indent=2, ensure_ascii=False)

    return response


@app.route('/newsapi', methods=['GET'])
def newsapi(): 
   
    newsapi = NewsApiClient(api_key='9d6dbf7235634000a185070d8e60cec0')
    #top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                      sources='bbc-news',
    #                                      category='business',
    #                                      language='en',
    #                                      country='us')

    all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)


    sources = newsapi.get_sources()
    return sources


@app.route('/nlpVoiceOver', methods=['GET'])
def nlpVoiceOver(): 
   news = request.args.get('news')
   language = 'hi'
   myobj = gTTS(text=news,lang=language,slow=False)
   dirpath = os.path.dirname(os.path.abspath(__file__))
   filepath = dirpath + "\\Voices\\news.mp3"
   filepath = filepath.replace("\\","/")
   myobj.save(filepath)
   os.system("start " + filepath)

