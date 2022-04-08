import base64
import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
import json
import random

class server():
    def __init__(self):
        # initializing flask
        self.app = Flask(__name__)
        CORS(self.app)
        self.file_name = "DirectionalStockPrediction"
        
        # adding routes
        self.app.add_url_rule("/predict", view_func=self.predict_inference, methods=["POST"])
        
        # starting flask server
        self.host = "10.0.2.15"
        self.app.run(host=self.host)

    # Function to call for "/predict" route
    def predict_inference(self):
        #if request.method == "POST":
            # response = {"inference": f"{inference}"}
            # response = json.dumps(response)
            # return Response(response=response, status=200, mimetype="application/json")
        pass
    
if __name__ == "__main__":
    server()
