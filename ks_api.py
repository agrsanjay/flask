
import base64
from pytz import timezone
import json
import requests
import pandas as pd
from parameter import get_fno_instrument_token
import datetime as dt

IST = timezone('Asia/Kolkata')

def get_ohlc(exchange="NSE",token=None,start_date=None,end_date=None,candle_interval=1):

    data = {
    "exchange": exchange,
    "wtoken": str(token),
    "fromdate": str(start_date),
    "todate": str(end_date),
    "interval": str(candle_interval)}
    data=base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    response = requests.get("https://ksapi.kotaksecurities.com/newserviceapi/cmots/equity/IntradayIntervalData/i/"+data)
    
    if response.status_code == 200:
        data = response.json()["result"]["IntradayIntervalData"]["IntradayIntervalData"]
        data = pd.DataFrame(data)
        data['tradedate'] =  pd.to_datetime(data['tradedate'], infer_datetime_format=True)
        data.rename(columns = {'DayOpen':'open', 'DayHigh':'high', 'DayLow':'low' , "last_price":"close",
                              'tradedate':'date'}, inplace = True)
        

        data = data.astype({'open':'float','high':'float','low':'float','close':'float'})
        data = data.set_index('date')
        
        #data.drop('co_code', axis=1, inplace=True)
        return data
    else:
        raise Exception("OHLC Api Error")

def get_combined_data(ce_strike,pe_strike,is_supertrend=None,days=0,index_symbol=None,expiry_date=None):

    
    
    ce_token = get_fno_instrument_token(index_symbol,expiry_date,ce_strike,"CE")
    pe_token = get_fno_instrument_token(index_symbol,expiry_date,pe_strike,"PE")
    sd = dt.datetime.now(tz=IST) - dt.timedelta(days=days)
    ed = dt.datetime.now(tz=IST)
    
    
    ce_data = get_ohlc(token=ce_token,start_date=sd,end_date=ed,candle_interval=1)
    pe_data = get_ohlc(token=pe_token,start_date=sd,end_date=ed,candle_interval=1)

    

    dates = list(set(ce_data.index.to_list()).intersection(set(pe_data.index.to_list())))
    dates = sorted(dates)
    ce_data = ce_data.loc[ce_data.index.isin(dates)]
    pe_data = pe_data.loc[pe_data.index.isin(dates)]
    ce_data['date'] = ce_data.index
    pe_data['date'] = pe_data.index
    combined_data = pd.DataFrame()
    combined_data['date'] = ce_data.index
    
    
    low = []
    high = []
    open = []
    close = []
    volume = []
    for i in dates:
        volume.append(float(ce_data['volume'][i]+pe_data["volume"][i])/2)
        close.append(ce_data['close'][i]+pe_data["close"][i])
        open.append(ce_data['open'][i]+pe_data["open"][i])
        low.append(min([ce_data['open'][i]+pe_data["open"][i],ce_data['close'][i]+pe_data["close"][i],ce_data['high'][i]+pe_data["low"][i],ce_data['low'][i]+pe_data["high"][i]]))
        high.append(max([ce_data['open'][i]+pe_data["open"][i],ce_data['close'][i]+pe_data["close"][i],ce_data['high'][i]+pe_data["low"][i],ce_data['low'][i]+pe_data["high"][i]]))
         
    combined_data ['high'],combined_data ['low'] ,combined_data ['volume'] = pd.DataFrame(high),pd.DataFrame(low),pd.DataFrame(volume)
    combined_data ['open'],combined_data ['close']  = pd.DataFrame(open),pd.DataFrame(close)
        
    return combined_data,ce_data,pe_data
