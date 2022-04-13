from cmath import exp
from sklearn.preprocessing import StandardScaler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import base64
import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
import json
import random
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import emoji
import re
import contractions
import pickle
import nltk
import os
import gensim
from transformers import BertTokenizer


# nltk.download('vader_lexicon')


class server():
    cwd = os.getcwd()+"/cse573-stock-prediction/code/server/"
    cwdM2 = os.getcwd()+"/cse573-stock-prediction/code/method2"
    def __init__(self):
        # initializing flask
        self.app = Flask(__name__)
        CORS(self.app)
        self.file_name = "DirectionalStockPrediction"

        # adding routes
        self.app.add_url_rule(
            "/predict", view_func=self.predict_inference, methods=["POST"])
        self.app.add_url_rule(
            "/tweets", view_func=self.predict_inference, methods=["POST"])

        # starting flask server
        self.host = "192.168.0.199"
        self.app.run(host=self.host)
        

    # Function to call for "/predict" route
    def predict_inference(self):
        if request.method == "POST":
            data = request.get_json(force=True)
            tweetURL = data["tweetURL"]
            options = Options()
            options.headless = True

            ### ! change path to match your own path ! ###
            CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"

            driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
            driver.get('https://publish.twitter.com/?query=' + tweetURL)
            soup = BeautifulSoup(driver.page_source, "lxml")
            item = soup.find('code', attrs={"class": "EmbedCode-code"})
            embed = item.contents[0]
            text = soup.find_all("p")[-1].get_text()
            tweetText = text
            print(tweetText)
            # response = {"result": f"{embed}"}
            response = {"result": f"{embed}",
                        "m1prediction": self.predict_direction1(tweetText),
                        "m2prediction": self.predict_direction2(tweetText),
                        "m3prediction": self.predict_direction3(tweetText)
                    }  
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")

    def predict_model1(self,text):
        sid = SentimentIntensityAnalyzer()
        scaler = StandardScaler()

        # load in trained logistic regression model
        file = open(self.cwd + 'lr.sav', 'rb')
        model = pickle.load(file)
        file.close()

        # load in trained w2v model
        w2v_file = open(self.cwd + 'w2v_model.sav', 'rb')
        w2v_model = pickle.load(w2v_file)
        w2v_file.close()

        # create the feature vector
        words_set = set(w2v_model.wv.index_to_key)
        tokens = text.split()
        X_vect = np.array([w2v_model.wv[i] for i in tokens if i in words_set])
        X_vect_avg = []
        if X_vect.size:
            X_vect_avg.append(np.append(X_vect.mean(axis=0),
                              sid.polarity_scores(text)['compound']))
        else:
            X_vect_avg.append(
                np.append(np.zeros(100, dtype=float), sid.polarity_scores(text)['compound']))
        X_vect_scale = scaler.fit_transform(X_vect_avg)

        # run prediction on trained model
        prediction = model.predict(X_vect_scale)[0]

        return prediction


    def bert_preprocess(text):

        # lowercase
        text = text.lower()
        # remove emojis
        text = emoji.get_emoji_regexp().sub(u'',text)
        # remove '\n'
        text =re.sub('\n',' ',text)
        # remove links
        text = re.sub('http\S+', 'LINK',text)
        # remove hashtags
        text = re.sub('\B\#\w+','HASHTAG',text)
        # remove @
        text = re.sub('\B\@\w+','AMPERSAND',text)
        # remove $
        text = re.sub('\B\$\w+','DOLLARSIGN',text)
        # remove extra whitespace
        text = re.sub(' +',' ',text)
        text = text.strip()
        # remove stop words

        return text


    def predict_model2(self,text):
        sid = SentimentIntensityAnalyzer()
        
        #load logistic regression model
        file = open(self.cwd + 'bert_logreg.sav','rb')
        model = pickle.load(file)
        file.close()

        #tokenize text
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        tokenized = tokenizer(text, padding=True)

        X = []
        X.append(sid.polarity_scores(text)['compound'])
        for i in tokenizer(text, padding=True)['input_ids']:
            X.append(i)
        
        for i in range(154-len(tokenizer(text, padding=True)['input_ids'])):\
            X.append(0)

        prediction = model.predict([X])

        return prediction


    def predict_model3(self,text):
        sid = SentimentIntensityAnalyzer()
        scaler = StandardScaler()

        # topic model
        tm_file = open(self.cwd + 'topic_model.sav', 'rb')
        tm_model = pickle.load(tm_file)
        tm_file.close()

        # words
        word_file = open(self.cwd + 'tm_words.sav', 'rb')
        words = pickle.load(word_file)
        word_file.close()

        # id2word
        id2word_file = open(self.cwd + 'tm_id2word.sav', 'rb')
        id2word = pickle.load(id2word_file)
        id2word_file.close()

        # corpus
        corpus_file = open(self.cwd + 'tm_corpus.sav', 'rb')
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
        file = open(self.cwd + 'lr_topic_model.sav', 'rb')
        model = pickle.load(file)
        file.close()
        prediction = model.predict(X_vect_scale)[0]

        return prediction

    def preprocess_text(self,text):
        # lowercase
        preprocess = text.lower()
        # remove emoji
        preprocess = emoji.get_emoji_regexp().sub(u'', preprocess)
        # remove new line
        preprocess = re.sub('\n', ' ', preprocess)
        # replace with tokens
        preprocess = re.sub('http\S+', 'LINK', preprocess)
        preprocess = re.sub('\B\#\w+', 'HASHTAG', preprocess)
        preprocess = re.sub('\B\@\w+', 'AMPERSAND', preprocess)
        preprocess = re.sub('\B\$\w+', 'DOLLARSIGN', preprocess)

        # expand contractions
        temp = preprocess.split()
        expanded_text = []
        for word in temp:
            expanded_text.append(contractions.fix(word))
        preprocess = ' '.join(expanded_text)

        # remove extra whitespace
        preprocess = re.sub(r'[^\w\s]', ' ', preprocess)
        preprocess = re.sub(' +', ' ', preprocess)
        preprocess = preprocess.strip()

        return preprocess

    def predict_direction(self,text):
        
        preprocess = self.preprocess_text(text)

        # model 1 prediction
        prediction_1 = self.predict_model1(preprocess)

        #model 2
        prediction_2 = self.predict_model2(preprocess)

        #model 3
        prediction_3 = self.predict_model3(preprocess)

        return str(prediction_1) + str(prediction_2) + str(prediction_3)

    def predict_direction1(self,text):
        
        preprocess = self.preprocess_text(text)

        # model 1 prediction
        prediction_1 = self.predict_model1(preprocess)

        # returns 0 or 1
        return str(prediction_1) 

    def predict_direction2(self,text):
        
        preprocess = self.preprocess_text(text)

        # model 1 prediction
        prediction_2 = self.predict_model2(preprocess)

        # returns [0] or [1]
        return str(prediction_2) 

    def predict_direction3(self,text):
        
        preprocess = self.preprocess_text(text)

        # model 3 prediction
        prediction_3 = self.predict_model3(preprocess)

        # return 0 or 1
        return str(prediction_3) 

if __name__ == "__main__":
    server()
    

