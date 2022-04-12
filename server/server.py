import base64
import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
import json
import random
import requests
import twint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class server():
    def __init__(self):
        # initializing flask
        self.app = Flask(__name__)
        CORS(self.app)
        self.file_name = "DirectionalStockPrediction"
        
        # adding routes
        self.app.add_url_rule("/predict", view_func=self.predict_inference, methods=["POST"])
        self.app.add_url_rule("/tweets", view_func=self.get_tweets, methods=["POST"])
        
        # starting flask server
        self.host = "10.0.2.15"
        self.app.run(host=self.host)

    # Function to call for "/predict" route
    def predict_inference(self):
        if request.method == "POST":
            data = request.get_json(force=True)
            tweetURL = data["tweetURL"]
            options = Options()
            options.headless = True
            CHROMEDRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"
            driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
            driver.get('https://publish.twitter.com/?query=' + tweetURL)
            soup = BeautifulSoup(driver.page_source, "lxml")
            item = soup.find('code', attrs={"class":"EmbedCode-code"})
            embed = item.contents[0]
            response = {"result": f"{embed}"}
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
    
if __name__ == "__main__":
    server()
