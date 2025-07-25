#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-12Dec-01
Modified on 2020-01Jan-21
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to parse out World Cup News.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2017-12-01       RWM        Initial Stub and Layout
    2020-03-21       RWM        Setting up on the new BBC website.
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

# Will Need to Update with new season update and promotions / relegations...
# Current as of 2017/18
def returnTeam(x):
    inputTeam = x
    outputTeam = 0
    if inputTeam == 'AFC Bournemouth' or inputTeam == 'Bournemouth':
        outputTeam = 1
    elif inputTeam == 'Arsenal':
        outputTeam = 2
    elif inputTeam == 'Aston Villa':
        outputTeam = 3
    elif inputTeam == 'Chelsea':
        outputTeam = 4
    elif inputTeam == 'Crystal Palace':
        outputTeam = 5
    elif inputTeam == 'Everton':
        outputTeam = 6
    elif inputTeam == 'Leicester City' or inputTeam == 'Leicester':
        outputTeam = 7
    elif inputTeam == 'Liverpool':
        outputTeam = 8
    elif inputTeam == 'Manchester City' or inputTeam == 'Man City':
        outputTeam = 9
    elif inputTeam == 'Manchester United' or inputTeam == 'Man Utd':
        outputTeam = 10
    elif inputTeam == 'Newcastle United' or inputTeam == 'Newcastle':
        outputTeam = 11
    elif inputTeam == 'Norwich City' or inputTeam == 'Norwich':
        outputTeam = 12
    elif inputTeam == 'Southampton':
        outputTeam = 13
    elif inputTeam == 'Stoke City' or inputTeam == 'Stoke':
        outputTeam = 14
    elif inputTeam == 'Sunderland':
        outputTeam = 15
    elif inputTeam == 'Swansea City' or inputTeam == 'Swansea':
        outputTeam = 16
    elif inputTeam == 'Tottenham Hotspur' or inputTeam == 'Tottenham':
        outputTeam = 17
    elif inputTeam == 'Watford':
        outputTeam = 18
    elif inputTeam == 'West Bromwich Albion' or inputTeam == 'West Brom':
        outputTeam = 19
    elif inputTeam == 'West Ham United' or inputTeam == 'West Ham':
        outputTeam = 20
    elif inputTeam == 'Burnley':
        outputTeam = 24
    elif inputTeam == 'Hull' or inputTeam == 'Hull City':
        outputTeam = 25
    elif inputTeam == 'Middlesbrough':
        outputTeam = 27
    elif inputTeam == 'Brighton' or inputTeam == 'Brighton & Hove Albion' or inputTeam == 'Brighton and Hove Albion':
        outputTeam = 28
    elif inputTeam == 'Huddersfield' or inputTeam == 'Huddersfield Town':
        outputTeam = 29
    elif inputTeam == 'Wolverhampton Wanderers' or inputTeam == 'Wolverhampton':
        outputTeam = 30
    elif inputTeam == 'Sheffield United' or inputTeam == 'Sheffield':
        outputTeam = 31
    else:
        outputTeam = 99
    return outputTeam

hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'English Premier League Parser ' + version
print(ds + ' :: ' + ts + ' :: ' + parseVersion)
print('Python Version :: ' + sys.version)
print(hr)

# Basic Parameters for the Season
seasonID = 5

# URLs to parse
bbcTeams = 'https://www.bbc.com/sport/football/teams'
bbcBase = 'http://www.bbc.com/sport/football/premier-league/scores-fixtures/'
seasonStart = '2020-06'

# Base Path for Output
localPath = 'F:\\Projects\\epl\\'
localimgPath = 'F:\\Projects\\epl\\img\\'

# Get match details
fixtureMonth = bbcBase + seasonStart
print (updateTS(), fixtureMonth)
fixtureObj = requests.get(fixtureMonth)
fixtureObj.raise_for_status()
fixtureSoup = bs4.BeautifulSoup(fixtureObj.text, "html.parser")

counter = 0

listOfFixtures = fixtureSoup.find_all('div')
while counter < 5:
    for i in listOfFixtures[2:]:
        print (i.prettify())
        print (shr)
        print (counter)
    counter += 1