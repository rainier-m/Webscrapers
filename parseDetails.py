#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-11Nov-09
Modified on 2017-11Nov-09
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2017-11-09       RWM        Initial Stub and Layout
'''

# Import Libraries needed for Scraping the various web pages
import bs4
import re
import datetime
import time
import requests
import webbrowser
import os
import openpyxl
import sys
import codecs
import mysql.connector

# Set Character Output
print ('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Establish MySQL Connection
cnx = mysql.connector.connect(user='root', password='password',
								 host='127.0.0.1',
								 database='fanfootball',
								 use_pure=False)

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print ('Downloading %s...' % (localFileName))
    with open(localimgPath + localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

# Visual Spacing Elements for Parsing
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version
parseVersion = 'Parse Stats Details v0.01.a'

# Websites to read and parse out...
