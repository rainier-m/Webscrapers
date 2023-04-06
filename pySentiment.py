#!python3
# -*- coding: utf-8 -*-
'''
Created on Jul 21, 2020
Modified on JUl 21, 2020
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to build Sentiment review for Day Trading information
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2020-07Jul-21    RWN        Initial Creation of the file to grab data and parse as needed

'''

# Import Libraries needed for Scraping the various web pages
import datetime
from decimal import Decimal
import csv
from bs4 import BeautifulSoup
# import requests
from urllib.request import urlopen, Request
import glob
import os
import sys
import time
import codecs
import mysql.connector
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import yfinance as yf
import pandas as pd
# import smtplib
# import ssl
# from get_all_tickers import get_tickers as gt
import shutil

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Establish MySQL Connection
cnx = mysql.connector.connect(user='user', password='password',
                              host='mjolnir',
                              database='daytrading',
                              auth_plugin='mysql_native_password')

if cnx.is_connected():
    db_Info = cnx.get_server_info()
    print("Successfully connected to DB v.", db_Info)

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")


# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Data Local Path & URLs
rhFileName = 'rh_sentiment.tar.gz'
reportPath = '\\DailyStockReport\\'
dataPath = '\\DailyStockReport\\Stocks\\'
globalPath = 'E:\\Google Drive\\Personal\\Daytrading'
rhRankedFile = globalPath + '\\DailyStockReport\\' + ds + '-OBV_Ranked.csv' # '2020-07-27-OBV_Ranked.csv'
# rhRankedFile = globalPath + '\\DailyStockReport\\' + '2020-10-05-OBV_Ranked.csv'
rhFilePathName = globalPath + '\\' + rhFileName
finwiz_url = 'https://finviz.com/quote.ashx?t='

# TO-DO
# Find most recent parsed file
print (ds)

#Parse the CSV to the Database
csvToParse = open(rhRankedFile)
csvReader = csv.reader(csvToParse)
csvData = list(csvReader)

def decimal_str(x: float, decimals: int = 10) -> str:
    return format(x, f".{decimals}").lstrip().rstrip('0')

# print (rhRankedFile)
# Parse File to SQL database
for row in csvData[1:]:
    tickerID = row[0]
    # print (row)
    OBV_Value = float(row[1])
    Close_Diff = float(decimal_str(row[2]))
    Spread = float(decimal_str(row[3]))
    Rank = float(decimal_str(row[4]))
    fileDate = datetime.datetime.now().strftime("%Y-%m-%d")
    # datetime.datetime(2020, 7, 20)

    # datetime.datetime.now().strftime("%Y-%m-%d")
    # print (tickerID, fileDate, obv_value, Close_Diff, Spread, Rank)
    # print ("INSERT INTO stock_obv_value (tickerID, obv_date, obv_value, close_diff, spread, ranked) VALUES (%s, %s, %s, %s, %s, %s)", (tickerID, fileDate, OBV_Value, Close_Diff, Spread, Rank))
    # exit()

    cursor = cnx.cursor()
    try:
        cursor.execute("INSERT INTO stock_obv_value (tickerID, obv_date, obv_value, close_diff, spread, ranked) "
                       "VALUES (%s, %s, %s, %s, %s, %s)", (tickerID, fileDate, OBV_Value, Close_Diff, Spread, Rank))
        print ("Row successfully added for:", fileDate, tickerID)
        cnx.commit()
    except Exception as e:
        print ("Row exists and did not insert for:", fileDate, tickerID)
        cnx.rollback()

# exit()
# TO DO
# ==============================
# 3. Save sentiment to SQL for the Day

news_tables = {}
# tickers = ['HTBX','TNXP','GLBS','GSAT','BOXL' ,'ONTX','PSV','XELA','NTEC','ATNM','IBIO','BKYI','GENE','ADMP','JAGX','BIOC','UMRX']

# SQL Query for Ticker
topN_sql = "select tickerID from stock_obv_value as a where a.obv_date = (select max(b.obv_date) from stock_obv_value as b) " \
            "and a.listed = 1 order by a.obv_date, a.ranked limit 250;"

cursor = cnx.cursor()
cursor.execute(topN_sql)
tickers = [row[0] for row in cursor.fetchall()]
counter = 0

# Read Headlines and Add to Dictionary
for ticker in tickers:
    url = finwiz_url + ticker
    print(url)
    req = Request(url=url, headers={'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
    # response = urlopen(req)
    try:
        response = urlopen(req)
    except (NameError, Exception) as e:
        sqlUpdate = "UPDATE stock_obv_value SET listed = 0 WHERE tickerID in \'%s\'" % ticker
        cursor.execute(sqlUpdate)
        cnx.commit()
        print(ticker, 'Error code: ', e.code)

    # BS4 Object from Request
    html = BeautifulSoup(response, "html.parser")

    # Get News-Table elements
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

parsed_news = []

# Parse headlines and create JSON for use by NLTK
for file_name, news_table in news_tables.items():
    try:
        newsfeed = news_table.findAll('tr')
    except Exception:
        newsfeed = ["<tr><td>Jan-01-00 00:00AM  </td><td><a href='\"No URL'\">No News Available</a></td></tr>"]

    # print(newsfeed)

    for x in newsfeed:
        # print(x)
        # print(shr)

        text = x.a.get_text()
        date_scrape = x.td.text.split()
        if len(date_scrape) == 1:
            time = date_scrape[0]
        else:
            date = date_scrape[0]
            time = date_scrape[1]
        ticker = file_name.split(' ')[0]
        parsed_news.append([ticker, date, time, text])

currentYear_parsed_news = []

for row in parsed_news:
    year = row[1][7:]
    month = row[1]
    # exit()
    # print (row[0], year)
    if year < '19':
        currentYear_parsed_news.append(row)

parsed_news[:] = [elem for elem in parsed_news if elem not in currentYear_parsed_news]

# print(parsed_news)
# Generate the Sentiment for each Stock Ticker
vader = SentimentIntensityAnalyzer()

# Generate Dataframe for Sentiment
columns = ['ticker', 'date', 'time', 'headline']
parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)
scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()
scores_df = pd.DataFrame(scores)
parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')
parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.to_period("D")

print(parsed_and_scored_news.head())
# Output sentiment to CSV file on reports
parsed_and_scored_news.to_csv('E:\\Google Drive\\Personal\\Daytrading\\DailyStockReport\\' + ds + '-Sentiment_Ranked.csv', index=False)

plt.rcParams['figure.figsize'] = [20, 10]

# Group by date and ticker columns from scored_news and calculate the mean
mean_scores = parsed_and_scored_news.groupby(['ticker', 'date']).mean()
# Unstack the column ticker
mean_scores = mean_scores.unstack()
# Get the cross-section of compound in the 'columns' axis
mean_scores = mean_scores.xs('compound', axis="columns").transpose()
# Plot a bar chart with pandas
mean_scores.plot(kind = 'bar')
plt.grid()

# plt.savefig(globalPath + reportPath + ds + '.png')
plt.savefig(globalPath + reportPath + ds + '.pdf')
