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
    2016-01Jan-15    RWN        Initial Creation of the file to parse out injuries and bans
                                from site. This is meant to parse out specific rumors and news
                                regarding BPL Players.
    2016-01Jan-17    RWN        Working to verify that only unique records are created to the DB.
    2016-01Jan-24    RWM        Working to add an Added TS to the table.
    2016-04Apr-19    RWM        Update the Table ID being used by the website for Injuries
    2016-09Sep-22    RWM        Deprecate the Excel usage in the module
    2016-10Oct-06    RWM        Cleaned up the Dates for updateDate, and returnDate
'''
# Import Libraries needed for Scraping the various web pages
import bs4
import re
import datetime
import requests
import os
import sys
import codecs
import mysql.connector

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
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
        print('Downloading %s...' % (localFileName))
    with open(localimgPath + localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True


hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'Premier League Injury & News Parser v0.01.a'
print(ds + ' :: ' + ts + ' :: ' + parseVersion)
print('Python Version :: ' + sys.version)
print(hr)

# Define URLs for the Barclay's Premier League
injuriesURL = 'http://www.fantasyfootballscout.co.uk/fantasy-football-injuries/'
teamNewsURL = 'http://www.fantasyfootballscout.co.uk/team-news/'
seasonID = 4

# Base Path for Output
localPath = 'F:\\ESPN-Parser\\'
localimgPath = 'F:\\ESPN-Parser\\img\\players\\'
# baseWkBk = 'stats_template.xlsx'
# workBook = openpyxl.load_workbook(os.path.join(localPath + baseWkBk))
# teamSheet = workBook.get_sheet_by_name('teams')
# playerSheet = workBook.get_sheet_by_name('players')
# matchSheet = workBook.get_sheet_by_name('matches')
# fixtureSheet = workBook.get_sheet_by_name('fixtures')
# newsSheet = workBook.get_sheet_by_name('news')
print (os.getcwd())

# Create BS4 Object from Injuries Web Page
injuryRes = requests.get(injuriesURL)
injuryRes.raise_for_status()
injurySoup = bs4.BeautifulSoup(injuryRes.text, "html.parser")
#with open(os.path.join(localPath + ds + '-injuryLanding.txt'), 'wb') as fo:
#    for chunk in injuryRes.iter_content(100000):
#        fo.write(chunk)


# Output Injury HTML Page.
# print (injurySoup.prettify())

# Download Image
def downloadImage(imageURL, localFileName):
    # print (localFileName)
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
    else:
        outputTeam = 99
    return outputTeam


newsUpdate = injurySoup.find("table", class_="ffs-ib respond ffs-ib-full-content ffs-ib-sort")
newsRows = newsUpdate.find_all("tr")

for i in newsRows:
    newsDetail = i.find_all("td")
    playerImage = i.find("img")
    playerImageID = ''
    counter = 0
    playerFirstName = ''
    playerName = ''
    playerTeam = ''
    playerStatus = ''
    returnDate = ''
    playerNews = ''
    newsURL = ''
    newsUpdated = ''
    for i in newsDetail:
        # if i is not None:
        # print (i)
        # print (counter)
        # print (shr)

        if counter == 0:
            playerName = i.get_text()
            playerName = playerName.strip()
            hasFirstName = playerName.find("(")
            if hasFirstName != -1:
                playerFirstName = playerName[playerName.find("(") + 1:len(playerName) - 1]
                # print (playerFirstName)
                playerName = playerName[:hasFirstName]
                playerName = playerName.strip()
            else:
                playerFirstName = ''
        if counter == 1:
            playerTeam = i["title"]
            playerTeam = returnTeam(playerTeam)
        if counter == 2:
            playerStatus = i.get_text()
        if counter == 3:
            returnDate = i.get_text()
            if len(returnDate) == 10:
                returnDate = returnDate[6:] + '-' + returnDate[3:5] + '-' + returnDate[0:2]
                # print (len(returnDate))
                # print (returnDate)
        if counter == 4:
            playerNews = i.get_text()
            playerNews = re.sub('   ', '', playerNews.lstrip())
            playerNews = re.sub('\[Source]$', '', playerNews)
            newsURL = i.find("a")
            if newsURL != None:
                newsURL = newsURL["href"]
            else:
                newsURL = ''
        if counter == 5:
            newsUpdated = i.get_text()
            newsUpdated = newsUpdated[6:] + '-' + newsUpdated[3:5] + '-' + newsUpdated[0:2]
            # print (newsUpdated)

        counter += 1
    if playerImage is not None:
        playerImage = playerImage["src"]
        imgFileName = playerImage[playerImage.rfind('/') + 1:]
        playerImage = playerImage
        # print (imgFileName)
        fileCheck = os.path.join(localimgPath, imgFileName)
        # print (fileCheck)
        playerImageID = imgFileName
        if os.path.isfile(fileCheck) == False:
            downloadImage(playerImage, imgFileName)
    else:
        playerImageID = "blank.jpg"
    print(playerFirstName, playerName, playerTeam, playerStatus, returnDate, playerNews, newsURL, newsUpdated,
          updateTS(), '1', seasonID, playerImageID)

    # Determine if record exists. If it does insert into Table
    cursor = cnx.cursor()
    cursor.execute(
        "SELECT player_firstname, player_name, player_team, player_news_status FROM stg_player_news WHERE player_firstname = %s AND player_name = %s AND player_team = %s ",
        (playerFirstName, playerName, playerTeam))
    results = cursor.fetchone()

    if results == None:
        cursor.execute(
            "INSERT INTO stg_player_news (player_firstname, player_name, player_team, player_status, player_returndate, player_news, player_newsURL, player_updateddate, player_rowadded, player_news_status, seasonID, player_imgID) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (playerFirstName, playerName, playerTeam, playerStatus, returnDate, playerNews, newsURL, newsUpdated,
             updateTS(), '1', seasonID, playerImageID))
        cnx.commit()
        print('Row added for %s and he is %s .' % (playerName, playerStatus))
    else:
        cursor.execute("UPDATE stg_player_news SET player_news_status = 1, player_rowadded = %s "
                       "WHERE player_firstname = %s AND player_name = %s AND player_team = %s ", (updateTS(), playerFirstName, playerName, playerTeam))
        cnx.commit()
        print('Row exists for %s and he is %s.' % (playerName, playerStatus))

        # print (counter)
    print(hr)
    # for i in newsDetail:
    # print (i)
    # print(shr)

# Commit and Close the Database Connection.
cnx.commit()
cnx.close()
print('MySQL Connection Closed')