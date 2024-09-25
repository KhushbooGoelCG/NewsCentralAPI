import json
import keyword
from urllib import response
import requests
import pandas as pd
import http.client
import openai

from flask import jsonify,request
from PythonFlaskAPI import app

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
    question = "cricket news"
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