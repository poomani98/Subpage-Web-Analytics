from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import json
import sys
import pandas as pd
import numpy as np

app = Flask(__name__)

heatmap = pd.read_csv("heatmap.csv",header=None)
events = pd.read_csv("events.csv")

CORS(app,resources={r"/*": {"origins": "*"}})

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/api', methods=['POST'])
def hello_python():
        js = request.get_json();
        #print(js, file=sys.stderr)
        #### do stuff
        for i in js['heatmap']:
          heatmap.iloc[round(i['y']/10),round(i['x']/10)] += 1
        for i in js['click']:
          events[i['element']][0]+=1
        events['scroll'][0]+=js['scroll']
        heatmap.to_csv("heatmap.csv",header=False,index=False)
        events.to_csv("events.csv",index=False)
        return "success"

if __name__ == '__main__':
   app.run()

