import os
from dotenv import load_dotenv
import requests
import json
import datetime
import pandas 
import math


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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



#capturing user input

import csv

#with open('portfolio.csv','w+') as file:
#    myFile=csv.writer(file)
#    myFile.writerow(["stock", "shares"])
#    noOfStocks=int(input("Please enter the number of different stocks you own: "))
#    for i in range (noOfStocks):
#        Stock=input("Company " + str(i +1)+ " : What is the ticker of the stock you own? ")
#        Shares=input("Company " + str(i +1)+ ": How many shares do you own? ")
#        myFile.writerow([Stock,Shares])


# 1. INFO INPUTS
from pandas import read_csv
df = read_csv('portfolio.csv')
#Stock= df["Stock"]
print(df.head())
portfolio=df.to_dict("records")
for row in portfolio:
    print(row)

    print(row["Stock"])


    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={row['Stock']}&apikey={ALPHAVANTAGE_API_KEY}"

    response = requests.get(request_url)

    parsed_response = json.loads(response.text)

    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys()) # TODO: sort to ensure latest day is first. currently assuming latest day is on top 

    latest_day = dates[0]

    latest_close = to_usd(float(tsd[latest_day]["4. close"]))
    latest_open = to_usd(float(tsd[latest_day]["1. open"]))
    print(f"LATEST CLOSE: {latest_close}")
    print(f"LATEST OPEN: {latest_open}")


#from pandas import read_csv
#df = read_csv("test.csv")
#print(df.head())


#col_list = ["Stock", "Shares"]
#df = pandas.read_csv('portfolio.csv',usecols=col_list)
#print(df)

#breakpoint()



# 2. INFO OUTPUTS


#print(f"SELECTED SYMBOL: {Stock}")
#print("-------------------------")
#print(f"SELECTED SYMBOL: {Stock}")

#print(latest_close)
#print(latest_open)

print(f"LATEST CLOSE: {latest_close}")
print(f"LATEST OPEN: {latest_open}")

print("test")


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")


def send_email(subject="[Daily Briefing] This is a test", html="<p>Hello World</p>", recipient_address=SENDER_EMAIL_ADDRESS):
    """
    Sends an email with the specified subject and html contents to the specified recipient,

    If recipient is not specified, sends to the admin's sender address by default.
    """
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)

    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=recipient_address, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e.message)
        return None


if __name__ == "__main__":
    subject = "Daily Portfolio Performance"

    html = f"""
    <h3>Daily Portfolio Performance Service</h3>

    <h4>Today's Date</h4>
    <p>Monday, January 1, 2040</p>

    <h4>My Stocks</h4>
    <ul>
        <li>MSFT | +3%</li>
        <li>GOOG | +2%</li>
        <li>AAPL | +4%</li>
    </ul>

    """

    send_email(subject, html)
