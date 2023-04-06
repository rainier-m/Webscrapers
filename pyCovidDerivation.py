#!python3
# -*- coding: utf-8 -*-
'''
Created on Jan 15, 2016
Modified on Oct 06, 2016
Version 0.03.ga
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2020-05May-15    RWN        Initial Creation of the file to parse out Covid Details to MySQL

'''

# Import Libraries needed for Scraping the various web pages
import re
import datetime
import csv
import os
import sys
import codecs
import mysql.connector
import pandas as pd

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())


# Establish MySQL Connection
cnx = mysql.connector.connect(user='user', password='password',
                              host='mjolnir',
                              database='covid_db',
                              auth_plugin='mysql_native_password')

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

country = 'US'
state = 'Florida'