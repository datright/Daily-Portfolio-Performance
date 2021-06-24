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

with open('portfolio.csv','w+') as file:
    myFile=csv.writer(file)
    myFile.writerow(["stock", "shares"])
    noOfStocks=int(input("Please enter the number of different stocks you own: "))
    for i in range (noOfStocks):
        Stock=input("Company " + str(i +1)+ " : What is the ticker of the stock you own? ")
        Shares=input("Company " + str(i +1)+ ": How many shares do you own? ")
        myFile.writerow([Stock,Shares])


# 1. INFO INPUTS

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={Stock}&apikey={ALPHAVANTAGE_API_KEY}"

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


print(prior_close)

import pandas
df = pandas.read_csv('portfolio.csv')
print(df)

#breakpoint()



# 2. INFO OUTPUTS)
int_latest = float(latest_close)
int_prior = float(prior_close)

daily_px = int_latest/int_prior-1
percentage = "{:.00%}".format(daily_px)
daily_pd = int_latest-int_prior


print(f"SELECTED SYMBOL: {stock}")
print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("REQUEST AT: ", current_time.strftime("%Y-%m-%d %I:%M %p"))
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"LATEST OPEN: {to_usd(float(latest_open))}")

print(f"PRIOR DAY CLOSE: {to_usd(float(prior_close))}")
print(f"DAILY $ CHANGE: ", to_usd(daily_pd))
print(f"DAILY % CHANGE: ", percentage)


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
