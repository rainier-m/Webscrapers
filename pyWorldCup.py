#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-12Dec-01
Modified on 2017-12Dec-01
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to parse out World Cup News.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2017-12-01       RWM        Initial Stub and Layout
'''

version = '0.01.a'

# Import Libraries needed for Scraping the various web pages
import datetime
import bs4
import requests
import pprint
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
cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='worldcup2018',
                              use_pure=False)

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
parseVersion = 'World Cup Parser ' + version
print(ds + ' :: ' + ts + ' :: ' + parseVersion)
print('Python Version :: ' + sys.version)
print(hr)

# URLs to parse
bbcBase = 'http://www.bbc.com/sport/football/world-cup/schedule/group-stage'

# Base Path for Output
localPath = 'D:\\worldcup\\'
localimgPath = 'D:\\worldcup\\img\\'

# Create BS4 object and parse to core file
scheduleRes = requests.get(bbcBase)
scheduleRes.raise_for_status()
scheduleSoup = bs4.BeautifulSoup(scheduleRes.text, "html.parser")

actSchedule = scheduleSoup.find("div", id="schedule-by-group")
groups = actSchedule.find_all("div", class_="group-stage__wrapper gel-layout gel-layout--center")
indv_group = actSchedule.find_all("div", class_="group-stage gel-layout__item")

print ("No of Groups:", len(indv_group))
print (shr)


for i in indv_group:
    # print(i.prettify())
    groups = i.find_all("h2")
    table = i.find_all("table")
    print (len(groups ))
    print (len(table))
    print(hr)
