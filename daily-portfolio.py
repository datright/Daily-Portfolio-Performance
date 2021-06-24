import os
from dotenv import load_dotenv
import requests
import json
import datetime
import pandas 
import math
load_dotenv()

current_time = datetime.datetime.now()
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

symbol = "MSFT"

# 1. INFO INPUTS

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"

response = requests.get(request_url)
#print(type(response)) #> requests.models.Response
#print(response.text) #> 200

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: sort to ensure latest day is first. currently assuming latest day is on top 

latest_day = dates[0]
prior_day = dates[1]
latest_close = tsd[latest_day]["4. close"]
latest_open = tsd[latest_day]["1. open"]
prior_close = tsd[prior_day]["4. close"]




#breakpoint()



# 2. INFO OUTPUTS)
int_latest = float(latest_close)
int_prior = float(prior_close)

daily_px = int_latest/int_prior-1
daily_pd = int_latest-int_prior

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", current_time.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"LATEST OPEN: {to_usd(float(latest_open))}")
print(f"PRIOR DAY CLOSE: {to_usd(float(prior_close))}")
print(f"DAILY $ CHANGE: ", to_usd(daily_px))
print(f"DAILY % CHANGE: ", daily_pd)
