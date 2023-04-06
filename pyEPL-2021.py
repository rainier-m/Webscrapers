#!python3
# -*- coding: utf-8 -*-
'''
Created on  2021-08Aug-12
Modified on 2021-08Aug-12
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to parse out World Cup News.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2021-08-21       RWM        Initial Stub and Layout
    2020-08-21       RWM        Setting up on the new SkySport website.
'''

version = '0.01.a'

# Import Libraries needed for Scraping the various web pages
import datetime
import bs4
import requests
import pandas as pd
import numpy as np
import sys
import codecs
import mysql.connector

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Establish MySQL Connection
cnx = mysql.connector.connect(user='user', password='password',
                              host='mjolnir',
                              database='fanfootball',
                              auth_plugin='mysql_native_password')

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
    with open(localimgPath + localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'English Premier League Parser ' + version
print(ds + ' :: ' + ts + ' :: ' + parseVersion)
print('Python Version :: ' + sys.version)
print(hr)

# Base Path for Output
localPath = 'E:\\Projects\\epl\\'
localimgPath = 'E:\\Projects\\epl\\img\\'

# Basic Parameters for the Season
seasonID = 6

# URLs for Scraping
baseFixturesURL = 'https://www.skysports.com/premier-league-fixtures'
baseResultsURL = 'https://www.skysports.com/premier-league-results'
baseEPLapi = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# Create BS4 Object from Fixtures Web Page
baseRes = requests.get(baseFixturesURL)
baseRes.raise_for_status()
fixturesSoup = bs4.BeautifulSoup(baseRes.text, "html.parser")
# print (fixturesSoup.prettify())

# Div Class to pull: <div class="grid__col site-layout-secondary__col1">
# Main container for fixtures
fixtureDiv = fixturesSoup.find_all("div", {"class": "grid__col site-layout-secondary__col1"})

# identify and extract the main containers for all fixtures
for i in fixtureDiv:
    fxtContainer = i
    blockFxt = fxtContainer.find_all("div", {"class": "fixres__body callfn"})
    blockItems = fxtContainer.find_all("div", {"class": "fixres__item"})
    # print(blockFxt)
    # iterate through fixtures in the container

    for i in blockItems:
        # print (i.prettify())
        content = i
        matchURL = content.find_all("a")
        for i in matchURL:
            print (i.prettify())
            # print (matchDate)
            print (shr)
        print (hr)
    print (len(blockItems))
    print (hr)