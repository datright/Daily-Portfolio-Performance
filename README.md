# Daily-Portfolio-Performance
Freestyle Project: Daily Stock Portfolio Performance by Jourdan Bua, Dat Hoang, Amanda Krichman, and Steven Shtaynberger

This should be run after market close to get an overview of your stock portfolio's performance for the day.

## Installation
Clone or download this repo onto your local computer.
Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):
```sh
cd daily-portfolio-performance
```

## Setup
Setup a virtual environment:
```sh
conda create -n my-portfolio-env python=3.8
conda activate my-portfolio-env
```
Install the required packages:
```sh
pip install -r requirements.txt
```
Create a portfolio.csv file with using the following set up (these are example stocks):
```sh
Stock,Shares
AAPL,10
NKE,5
```

### Configuring Environment Variables
Add a new ".env" file to the root directory of this repo, and place contents like the following inside:
```
PORTFOLIO_OWNER="Professor Rossetti"

ALPHAVANTAGE_API_KEY="your unique key"
```

## Usage
Run the portfolio:
```
python app/daily_portfolio.py
```
