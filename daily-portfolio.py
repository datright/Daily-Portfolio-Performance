import os
from dotenv import load_dotenv
import requests
import json
import datetime

import math
import pandas



#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail


load_dotenv()

PORTFOLIO_OWNER = os.getenv("PORTFOLIO_OWNER")

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

import datetime as dt
todays_date = dt.datetime.now()

#capturing user input

#import csv

#with open('portfolio.csv','w+') as file:

 #   myFile=csv.writer(file)
  #  myFile.writerow(["Stock", "Shares"])
   # noOfStocks=int(input("Please enter the number of different stocks you own: "))
    #for i in range (noOfStocks):
     #   Stock=input("Company " + str(i +1)+ " : What is the ticker of the stock you own? ")
      #  Shares=input("Company " + str(i +1)+ ": How many shares do you own? ")
       # myFile.writerow([Stock,Shares])

print ("-------------------")
print("Welcome "+ PORTFOLIO_OWNER + "!") 
print("Here is your updated stock portfolio as of "+ todays_date.strftime("%Y-%m-%d"))
print ("-------------------")

# 1. INFO INPUTS
Portfolio_change=0
Total_market=0
from pandas import read_csv
df = read_csv('portfolio.csv')
#Stock= df["Stock"]
print(df.head())
portfolio=df.to_dict("records")
for row in portfolio:


    print(row["Stock"])
    


    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={row['Stock']}&apikey={ALPHAVANTAGE_API_KEY}"

    response = requests.get(request_url)

    parsed_response = json.loads(response.text)

    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys()) # TODO: sort to ensure latest day is first. currently assuming latest day is on top 
    latest_day = dates[0]
    prior_day = dates[1]
    latest_close = tsd[latest_day]["4. close"]
    latest_open = tsd[latest_day]["1. open"]
    prior_close = tsd[prior_day]["4. close"]
    int_latest = float(latest_close)
    int_prior = float(prior_close)
    daily_px = int_latest/int_prior-1
    percentage = "{:.2%}".format(daily_px)
    daily_pd = int_latest-int_prior
    Total_change=row["Shares"]*daily_pd
    Market_Value=row["Shares"]*float(latest_close)
    Total_market=Total_market+Market_Value
    Portfolio_change=Portfolio_change+Total_change
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    #print(f"LATEST OPEN: {latest_open}")   
    #print(f"PRIOR DAY CLOSE: {to_usd(float(prior_close))}")
    print(f"DAILY $ CHANGE: ", to_usd(daily_pd))
    print(f"DAILY % CHANGE: ", percentage)
    print(f"TOTAL MARKET VALUE:", to_usd(float(Market_Value)))
    print(f"TOTAL STOCK CHANGE:", to_usd(float(Total_change)))
    print ("-------------------")

print(f"YOUR TOTAL STOCK PORTFOLIO CHANGE FOR THE DAY IS:", to_usd(float(Portfolio_change)))
print ("-------------------")
print(f"YOUR TOTAL STOCK PORTFOLIO IS WORTH:", to_usd(float(Total_market)))
print ("-------------------")
if Portfolio_change>0:
    print("WELL DONE. YOU'VE MADE SOME MONEY TODAY")
elif Portfolio_change==0:
    print("YOUR TOTAL PORTFOLIO VALUE HAS NOT CHANGED")
elif Portfolio_change<0:
    print("DON'T WORRY. THERE'S ALWAYS TOMORROW!")











    