import json
from account_config import *
import requests
import pandas as pd
import io
import datetime
from pytz import timezone

IST = timezone('Asia/Kolkata')

today_date= datetime.datetime.now(tz=IST)

print("Downloading Script Masters...")

response = requests.get('https://tradeapi.kotaksecurities.com/apim/scripmaster/1.1/filename', headers={
    'accept': 'application/json',
    'consumerKey': user_id,
    'Authorization': 'Bearer '+access_token,
})

response = json.loads(response.text)['Success']

fno_url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_09_12_2022.txt'
cash_url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_09_12_2022.txt'

fno_response = requests.get(fno_url)

fno_df = pd.read_csv(io.StringIO(fno_response.text), sep="|")


cash_response = requests.get(cash_url)

cash_df = pd.read_csv(io.StringIO(cash_response.text), sep="|")

fno_script_master = fno_df.loc[(fno_df['segment'] == "FO") ]
fno_script_master = fno_script_master.loc[(fno_script_master['instrumentType']=="OI")]

fno_script_master.to_csv("fno.csv")
