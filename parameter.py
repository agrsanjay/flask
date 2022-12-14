
import datetime
import pandas as pd
from pytz import timezone

try:
    fno_script_master = pd.read_csv("fno.csv")
except:
    from scrip_data import fno_script_master

IST = timezone('Asia/Kolkata')



def get_current_expiry_date(index_symbol,expiry ):
    df = fno_script_master
    df["expiry"] = pd.to_datetime(df["expiry"])
    scrip_master = (df.loc[df["instrumentName"] == index_symbol]).sort_values(by=["expiry"])
    expiry_dates = sorted(list(set(scrip_master['expiry'].to_list())))
    print(expiry_dates)
    return (expiry_dates[expiry]).strftime("%d%b%y").upper()







def get_fno_instrument_token(index_symbol,expiry,strike,optionType):
    
    script = fno_script_master['instrumentToken'].loc[(fno_script_master['instrumentName']==index_symbol) & (fno_script_master['expiry']==expiry) & (fno_script_master['strike'] == float(strike)) & (fno_script_master['optionType']==optionType)]
    return int(script.iloc[0])

def get_symbol_token(token):
    df = fno_script_master.loc[fno_script_master['instrumentToken']==token]
    return str(df["instrumentName"].iloc[-1])+"_"+str(int(df["strike"].iloc[-1]))+"_"+str(df["optionType"].iloc[-1])