from flask import Flask, request, Response
app = Flask(__name__)
import jsonpickle
app = Flask(__name__)
from Model import get_prediction_csv
import pickle
import pandas as pd
import io, os

@app.route("/predict_csv", methods=['POST', 'GET'])
def predict():
    # load csv file

    # run prediction
    output = get_prediction_csv("Data/CSV_test.csv")
    
    # serialize the data into a JSON string

    # return a response with a content type of JSON
    response = Response(jsonpickle.encode(output, unpicklable=False), mimetype='application/json')
    return response


@app.route("/")
def home():
    return "LITHOFACIES PREDICTIONS API"


if __name__ == '__main__':
    while True:
        try:
            app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 16000)))
        except Exception as e:
            print(e)
            print("restart....")


