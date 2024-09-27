import json
import keyword
from urllib import response
import requests
import pandas as pd
import http.client

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
