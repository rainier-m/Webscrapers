#!python3
# -*- coding: utf-8 -*-
'''
Created on Jul 20, 2020
Modified on JUl 20, 2020
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to build Day Trading information for review
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2020-07Jul-20    RWN        Initial Creation of the file to grab data and parse as needed

'''

# Import Libraries needed for Scraping the various web pages
import re
import datetime
import tarfile
import requests
import glob
import os
import sys
import time
import codecs
import mysql.connector
import yfinance as yf
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
    print("Successfully connected to DB", db_Info)

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

cursor = cnx.cursor()
cursor.execute("SELECT * FROM last_processed WHERE idLast_Processed = \'%s\'" % ds)
results = cursor.fetchone()

if results == None:
    print('No results...')
    try:
        cursor.execute("INSERT INTO last_processed (idLast_Processed) values (\'%s\')" % (ds))
        cnx.commit()
        print('Processed Date Added:', ds)
    except Exception as e:
        print('Already Processed Date:', ds)
        cnx.rollback()

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"


# Ticker Details
# tickers = gt.get_tickers_filtered(mktcap_min=150000, mktcap_max=160000)
RH_zipfileURL = 'https://robintrack-data.ameo.design/robintrack-popularity-history.tar.gz'

# Data Local Path
rhFileName = 'rh_sentiment.tar.gz'
dataPath = '\\DailyStockReport\\Stocks\\'
globalPath = 'E:\\Google Drive\\Personal\\Daytrading'
rhFilePathName = globalPath + '\\' + rhFileName

# Robinhood File download Download Zip File
def downloadFile(fileURL, localFileName):
    # print (localFileName)
    # dlProgress = 0
    response = requests.get(fileURL)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
    with open(globalPath + '\\' + localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
            # dlProgress += 4096
            # print ("Downloaded:", str(dlProgress))
    return True

# Clear and make directories for Local Data Processing
# shutil.rmtree(os.path.join(globalPath + dataPath))
# os.mkdir(os.path.join(globalPath + dataPath))
# downloadFile(RH_zipfileURL, rhFileName)

# Number of API Calls
API_Calls = 0

# Loop responsible for holding data fr each ticker in our list.
Stock_Failure  = 0
Stocks_NotImported = 0

# Iteration Variable
iter = 0

# Read Contents of Zip File
# Get existing Zip File and download if at least one day old.
if (os.path.isfile(rhFilePathName) == True) and (tarfile.is_tarfile(rhFilePathName) == True):
    print ("File Exists")
    today = datetime.datetime.today()
    modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(rhFilePathName))
    fileDateCheck = today - modified_date
    if fileDateCheck.days > 14:
        print ("File is older than a day! Getting new Sentiment File.")
        downloadFile(RH_zipfileURL, rhFileName)
        print("New Sentiment File downloaded:", rhFilePathName)

        rh_tarfile = tarfile.open(rhFilePathName)
        for i in rh_tarfile.getnames()[1:]:
            stockSymbol = i[22:]
            stockSymbol = stockSymbol[:len(stockSymbol)-4]
            # print (stockSymbol)

            cursor = cnx.cursor()
            # print ("SELECT tickerID FROM stocktickers WHERE tickerID = \'%s\'" % stockSymbol)
            cursor.execute("SELECT tickerID FROM stocktickers WHERE tickerID = \'%s\'" % stockSymbol)
            results = cursor.fetchone()

            if results  == None:
                print ('No results...')
                try:
                    cursor.execute("INSERT INTO stocktickers (tickerID) values (\'%s\')" % (stockSymbol))
                    cnx.commit()
                    print('Stock Ticker Added:', stockSymbol)
                except Exception as e:
                    print ('Row failed to insert:', stockSymbol)
                    cnx.rollback()

    else:
        print ("File is not older than a day. Using existing Sentiment File.")

# SQL to pull stock tickers to get data for from Yahoo Finance
cursor = cnx.cursor()
cursor.execute("SELECT tickerID FROM stocktickers")
results = cursor.fetchall()
tickers = results
print("The amount of stocks chosen to observe: " + str(len(tickers)))

searchStocks = 5 # len(tickers)
maxAPIcalls = 16000

while (iter < searchStocks) and (API_Calls < maxAPIcalls):
    stock = tickers[iter][0]
    today = datetime.datetime.today()
    stockFile =os.path.isfile(globalPath + dataPath + stock +".csv")
    if stockFile == True:
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(globalPath + dataPath + stock +".csv"))
    else:
        modified_date = datetime.datetime.today()
    fileDateCheck = today - modified_date
    print (fileDateCheck)

    # Find and remove files without a Ticker Response

    if (os.path.isfile(globalPath + dataPath + stock +".csv") == True) and (fileDateCheck.days > 5):
        print ("File Older than One Day")
        try:
            # stock = tickers[iter][0]
            temp = yf.Ticker(str(stock))
            Hist_data = temp.history(period="6mo")
            Hist_data.to_csv(globalPath + dataPath + stock +".csv")
            time.sleep(2)
            API_Calls += 1
            Stock_Failure = 0
            iter += 1
        except ValueError:
            print ("Yahoo Finance Backend Error, Attempting to Fix")
            if Stock_Failure > 5:
                iter += 1
                Stocks_NotImported += 1
            API_Calls += 1
            Stock_Failure += 1
        except:
            print ("Error returned...")
    elif (os.path.isfile(globalPath + dataPath + stock +".csv") != True):
        print("No File Exists", stock)
        try:
            # stock = tickers[iter][0]
            temp = yf.Ticker(str(stock))
            Hist_data = temp.history(period="6mo")
            Hist_data.to_csv(globalPath + dataPath + stock +".csv")
            time.sleep(2)
            API_Calls += 1
            Stock_Failure = 0
            iter += 1
        except ValueError:
            print ("Yahoo Finance Backend Error, Attempting to Fix")
            if Stock_Failure > 5:
                iter += 1
                Stocks_NotImported += 1
            API_Calls += 1
            Stock_Failure += 1
        except:
            print ("Error returned...")
    else:
        print("File isn't older than a day", stock)
        API_Calls += 1
        iter += 1
        Stock_Failure += 1
print("Stocks succesfully imported: " + str(iter - Stocks_NotImported))

# Get and review the pulled files and process them
list_files = (glob.glob(globalPath + dataPath + "*.csv"))
new_data = []
interval = 0
removeFromList = []

# Delete Empty Files
for file in list_files:
    if os.path.getsize(file) < 1024:
        os.remove(file)
        removeFromList.append(file)

list_files[:] = [elem for elem in list_files if elem not in removeFromList]

while interval < len(list_files):
    Data = pd.read_csv(list_files[interval])  # Gets the last 10 days of trading for the current stock in iteration
    Data.sort_values("Date", inplace = True, ascending = False)
    print(list_files[interval])
    pos_move = []  # List of days that the stock price increased
    neg_move = []  # List of days that the stock price increased
    OBV_Value = 0  # Sets the initial OBV_Value to zero
    Close_Diff = 0 # Sets the initial Daily Close Difference to zero
    Spread = 0 # Sets the initial Daily Spread to zero
    plus_minus = 1 # Identifies Up or Down Tick
    count = 0
    while (count < 20):  # 10 because we are looking at the last 10 trading days
        print(Data.iloc[count, 1], Data.iloc[count, 2], Data.iloc[count, 3])
        if Data.iloc[count, 1] < Data.iloc[count, 4]:  # True if the stock increased in price
            pos_move.append(count)  # Add the day to the pos_move list
        elif Data.iloc[count, 1] > Data.iloc[count, 4]:  # True if the stock decreased in price
            neg_move.append(count)  # Add the day to the neg_move list
        count += 1
    count2 = 0
    # print (pos_move)
    for i in pos_move:  # Adds the volumes of positive days to OBV_Value, divide by opening price to normalize across all stocks
        OBV_Value = round(OBV_Value + (Data.iloc[i,5]/Data.iloc[i,1]))
        Close_Diff = Close_Diff + (Data.iloc[i, 1] - Data.iloc[i,4])
        Spread = Spread + (Data.iloc[i, 2] - Data.iloc[i, 3])
    for i in neg_move:  # Subtracts the volumes of negative days from OBV_Value, divide by opening price to normalize across all stocks
        OBV_Value = round(OBV_Value - (Data.iloc[i,5]/Data.iloc[i,1]))
        Close_Diff = Close_Diff + (Data.iloc[i, 1] - Data.iloc[i, 4])
        Spread = Spread + (Data.iloc[i, 2] - Data.iloc[i, 3])
    Stock_Name = ((os.path.basename(list_files[interval])).split(".csv")[0])  # Get the name of the current stock we are analyzing
    new_data.append([Stock_Name, OBV_Value, Close_Diff, Spread])  # Add the stock name and OBV value to the new_data list
    interval += 1
df = pd.DataFrame(new_data, columns = ['Stock', 'OBV_Value', 'Close Diff', 'Spread'])  # Creates a new dataframe from the new_data list
df["Stocks_Ranked"] = df["OBV_Value"].rank(ascending = False)  # Rank the stocks by their OBV_Values
df.sort_values("OBV_Value", inplace = True, ascending = False)  # Sort the ranked stocks
df.to_csv(globalPath + "\\DailyStockReport\\" + ds + "-OBV_Ranked.csv", index = False)  # Save the dataframe to a csv without the index column



cnx.close()