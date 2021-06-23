import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")



#capturing user input

import csv

with open('portfolio.csv','w+') as file:
    myFile=csv.writer(file)
    myFile.writerow(["Stock", "Shares"])
    noOfStocks=int(input("Please enter the number of different stocks you own: "))
    for i in range (noOfStocks):
        Stock=input("Company " + str(i +1)+ " : What is the ticker of the stock you own? ")
        Shares=input("Company " + str(i +1)+ ": How many shares do you own? ")
        myFile.writerow([Stock,Shares])


# 1. INFO INPUTS

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={Stock}&apikey={ALPHAVANTAGE_API_KEY}"

response = requests.get(request_url)

parsed_response = json.loads(response.text)

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: sort to ensure latest day is first. currently assuming latest day is on top 

latest_day = dates[0]

latest_close = to_usd(float(tsd[latest_day]["4. close"]))
latest_open = to_usd(float(tsd[latest_day]["1. open"]))



from pandas import read_csv
df = read_csv("portfolio.csv")
print(df.head())


#col_list = ["Stock", "Shares"]
#df = pandas.read_csv('portfolio.csv',usecols=col_list)
#print(df)

#breakpoint()



# 2. INFO OUTPUTS


#print(f"SELECTED SYMBOL: {stock}")


print(f"LATEST CLOSE: {latest_close}")
print(f"LATEST OPEN: {latest_open}")

