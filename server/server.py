import base64
from cmath import exp
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
import emoji
import re
import contractions
import pickle
import nltk
from transformers import BertTokenizer
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.preprocessing import StandardScaler




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
        
    def get_tweets(self):
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

    def predict_model1(text):
        sid = SentimentIntensityAnalyzer()
        scaler = StandardScaler()

        # load in trained logistic regression model
        file = open('lr.sav','rb')
        model = pickle.load(file)
        file.close()

        # load in trained w2v model
        w2v_file = open('w2v_model.sav','rb')
        w2v_model = pickle.load(w2v_file)
        w2v_file.close()

        # create the feature vector
        words_set = set(w2v_model.wv.index_to_key)
        tokens = text.split()
        X_vect = np.array([w2v_model.wv[i] for i in tokens if i in words_set])
        X_vect_avg = []
        if X_vect.size:
            X_vect_avg.append(np.append(X_vect.mean(axis=0),sid.polarity_scores(text)['compound']))
        else:
            X_vect_avg.append(np.append(np.zeros(100, dtype=float),sid.polarity_scores(text)['compound']))
        X_vect_scale = scaler.fit_transform(X_vect_avg)

        # run prediction on trained model
        prediction = model.predict(X_vect_scale)[0]
        
        return prediction

    def predict_model2(text):
        sid = SentimentIntensityAnalyzer()
        
        #load logistic regression model
        file = open('bert_logreg.sav','rb')
        model = pickle.load(file)
        file.close()

        #tokenize text
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        tokenized = tokenizer(text, padding=True)

        X = []
        X.append(sid.polarity_scores(text)['compound'])
        for i in tokenizer(text, padding=True)['input_ids']:
            X.append(i)
        
        for i in range(153-len(tokenizer(text, padding=True)['input_ids'])):\
            X.append(0)

        prediction = model.predict([X])

        return prediction


    def predict_model3(text):
        sid = SentimentIntensityAnalyzer()
        scaler = StandardScaler()

        # topic model
        tm_file = open('topic_model.sav','rb')
        tm_model = pickle.load(tm_file)
        tm_file.close()

        # words
        word_file = open('tm_words.sav','rb')
        words = pickle.load(word_file)
        word_file.close()

        # id2word
        id2word_file = open('tm_id2word.sav','rb')
        id2word = pickle.load(id2word_file)
        id2word_file.close()

        # corpus
        corpus_file = open('tm_corpus.sav','rb')
        corpus = pickle.load(corpus_file)
        corpus_file.close()

        # create feature vector 
        split_text = text.split()
        new_text = id2word.doc2bow(split_text)
        topics = tm_model.get_document_topics(new_text,
                                            minimum_probability=0.0)
        features = [topics[i][1] for i in range(70)]
        features.append(sid.polarity_scores(text)['compound'])
        X_vect_scale = scaler.fit_transform([features])

        # run prediction on trained model
        file = open('lr_topic_model.sav','rb')
        model = pickle.load(file)
        file.close()
        prediction = model.predict(X_vect_scale)[0]

        return prediction

    def preprocess_text(text):
        # lowercase
        preprocess = text.lower()
        # remove emoji
        preprocess = emoji.get_emoji_regexp().sub(u'',preprocess)
        # remove new line
        preprocess = re.sub('\n',' ',preprocess)
        # replace with tokens
        preprocess = re.sub('http\S+', 'LINK', preprocess)
        preprocess = re.sub('\B\#\w+','HASHTAG',preprocess)
        preprocess = re.sub('\B\@\w+','AMPERSAND',preprocess)
        preprocess = re.sub('\B\$\w+','DOLLARSIGN',preprocess)

        # expand contractions
        temp = preprocess.split()
        expanded_text = []
        for word in temp:
            expanded_text.append(contractions.fix(word))
        preprocess = ' '.join(expanded_text)

        # remove extra whitespace
        preprocess = re.sub(r'[^\w\s]',' ',preprocess)
        preprocess = re.sub(' +', ' ',preprocess)
        preprocess = preprocess.strip()

        return preprocess

    def predict_direction(text):
            preprocess = preprocess_text(text)
            
            # model 1 prediction
            prediction_1 = predict_model1(preprocess)
        
            #model 2
            prediction_2 = predict_model2(preprocess)

            #model 3
            prediction_3 = predict_model3(preprocess)

            return [prediction_1,prediction_2,prediction_3]


if __name__ == "__main__":
    server()
