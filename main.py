from flask import Flask, jsonify,request
import os
from flask_cors import CORS
import json
import ks_api
from parameter import *


app = Flask(__name__)
CORS(app)


def make_json(data):
    
    # create a dictionary
    data['date'] =data['date'].astype(str)
    new_data = {
        "date": data['date'].to_list(),
         "open": data['open'].to_list(),
          "high": data['high'].to_list(),
           "low": data['low'].to_list(),
            "close": data['close'].to_list(),
            "volume": data['volume'].to_list(),
            #"supertrend": data['supertrend'].to_list()
    }
    return new_data


@app.route('/ohlc', methods=['POST'])
def get_ohlc_data():
    req = json.loads(request.data)
    index_symbol = req['index_symbol']
    ce_strike = req["ce_strike"]
    pe_strike = req["pe_strike"]
    days = int(req['days'])
    expiry_date = get_current_expiry_date(index_symbol)
    data = ks_api.get_combined_data(ce_strike,pe_strike,is_supertrend=None,days=days,index_symbol=index_symbol,expiry_date=expiry_date)
    
    data = make_json(data)
    
    return data


@app.route('/')
def index():
    print(request.data)
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
