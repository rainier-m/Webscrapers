#!python3
# -*- coding: utf-8 -*-
'''
Created on May 19, 2018
Modified on May 19, 2018
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2018-05May-19    RWM        Initial stub and build out of webscraper

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
                              database='worldcup2018',
                              use_pure=False)
# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Visual Separators for Output
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'World Cup Web Parser v0.01.a'
print(ds + ' :: ' + ts + ' :: ' + parseVersion)
print('Python Version :: ' + sys.version)
print(hr)

# Setup default web URLs for scraping
baseWC = 'https://www.bbc.com/sport/football/world-cup'
scheduleWC = 'https://www.bbc.com/sport/football/world-cup/schedule/group-stage'
knockoutWC = 'https://www.bbc.com/sport/football/world-cup/schedule/knockout-stage'
scoresWC = 'https://www.bbc.com/sport/football/world-cup/scores-fixtures'
teamRosters = 'https://www.bbc.com/sport/football/44083365'
parseMatch = 'https://www.bbc.com/sport/football/44258022'

# Base Path for Output
localPath = 'D:\\WorldCup-Parser\\'
localimgPath = 'D:\\WorldCup-Parser\\img\\'

# Download Images from a passed image URL, give a local filename + extension
def downloadImage(imageURL, localFileName):
    # print (localFileName)
    response = requests.get(imageURL)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
    with open(localimgPath + localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

# Function to return a two digit month for a literal Month (i.e., change "August" to "08").
def returnMonth(x):
    inputMonth = x
    inputMonth = inputMonth[0:3]
    outputMonth = ''
    # print inputMonth
    if inputMonth == 'Aug':
        outputMonth = '08'
    elif inputMonth == 'Sep':
        outputMonth = '09'
    elif inputMonth == 'Oct':
        outputMonth = '10'
    elif inputMonth == 'Nov':
        outputMonth = '11'
    elif inputMonth == 'Dec':
        outputMonth = '12'
    elif inputMonth == 'Jan':
        outputMonth = '01'
    elif inputMonth == 'Feb':
        outputMonth = '02'
    elif inputMonth == 'Mar':
        outputMonth = '03'
    elif inputMonth == 'Apr':
        outputMonth = '04'
    elif inputMonth == 'May':
        outputMonth = '05'
    elif inputMonth == 'Jun':
        outputMonth = '06'
    else:
        outputMonth = '07'
    return outputMonth

def returnDay(x):
    inputDay = x
    outputDay = inputDay[:3]
    return outputDay

def returnCountry(x):
    inputName = x
    outputName = ''
    cursor = cnx.cursor()
    sqlQuery = "SELECT team_id FROM teams WHERE team_long_name = '%s'" % inputName
    # print (sqlQuery)
    cursor.execute(sqlQuery)
    results = cursor.fetchone()
    if results != None:
        outputName = results[0]
    else:
        outputName = '999'
    # print (type(outputName))
    return outputName

# Create BS4 Object from Group Stage
scheduleRes = requests.get(scheduleWC)
scheduleRes.raise_for_status()
scheduleSoup = bs4.BeautifulSoup(scheduleRes.text, "html.parser")
with open(os.path.join(localPath + ds + '-groupStage_Landing.txt'), 'wb') as fo:
    for chunk in scheduleRes.iter_content(100000):
        fo.write(chunk)

# Output Injury HTML Page.
# print (scheduleSoup.prettify())

def teamInsert(container):
    teamContainer = container
    group = teamContainer.find('h2')
    group = group.get_text(strip=True)
    group = group[len(group)-1:]
    print ("The current Group is:", group)
    print (shr)
    groupTable = teamContainer.find('table')
    groupHead = groupTable.find('thead')
    headRow = groupHead.find_all('th')
    # print (len(headRow))
    # for i in headRow:
        # print (i)
    # print (shr)
    groupBody = groupTable.find('tbody')
    # print (groupBody.prettify())
    # print (len(groupHead))
    tableRow = groupBody.find_all('tr')
    for i in tableRow:
        # print (i)
        rowHead = i.find('th')
        rowImg = rowHead.find('img')
        rowImg = rowImg['src']
        imgName = rowImg[len(rowImg)-7:]
        fileCheck = os.path.join(localimgPath, imgName)
        if os.path.isfile(fileCheck) == False:
            downloadImage(rowImg, imgName)
        rowTitle = rowHead.find('abbr')
        rowAbbr = rowTitle.get_text(strip=True)
        rowTitle = rowTitle['title']
        urlLink = re.sub(" ", "-", rowTitle.lower())
        # print (urlLink)
        rowResults = i.find_all('td')
        rowWins = rowResults[0].get_text(strip=True)
        rowDraws = rowResults[1].get_text(strip=True)
        rowLosses = rowResults[2].get_text(strip=True)
        rowGoalDiff = rowResults[3].get_text(strip=True)
        rowPoints = rowResults[4].get_text(strip=True)
        # print (rowResults)
        # print (rowAbbr, rowTitle, rowWins, rowDraws, rowLosses, rowGoalDiff, rowPoints)
        # print (rowImg[len(rowImg)-7:])
        cursor = cnx.cursor()
        sqlQuery = "SELECT team_short_id, team_long_name FROM teams WHERE team_short_id = '%s'" % rowAbbr
        # print (sqlQuery)
        cursor.execute(sqlQuery)
        results = cursor.fetchone()
        # print (results)
        if results == None:
            cursor.execute("INSERT INTO teams (team_short_id, team_long_name, team_badge, team_URL, team_active_ind, team_updated) "
                           "VALUES (%s, %s, %s, %s, 1, date(%s))", (rowAbbr, rowTitle, imgName, urlLink, ds))
            cnx.commit()
            print (rowAbbr, rowTitle)

    # Get UL and parse group stage matches
    groupMatches = teamContainer.find('ul')
    # print (groupMatches.prettify())
    groupFixtures = groupMatches.find_all('li')
    for i in groupFixtures:
        fixtureDate = i.find('h3').get_text(strip=True)
        firstSpace = fixtureDate.find(" ")
        remainString = fixtureDate[firstSpace+1:]
        secondSpace = remainString.find(" ")
        ordinalDate = remainString[:secondSpace-2]
        strMonth = remainString[secondSpace+1:]
        dayOfWeek = fixtureDate[:firstSpace]
        details = i.find('div')
        location = i.find_all('span')
        location = location[4].get_text()
        # print (details.prettify())
        homeTeam = details.find("span", class_='home_team').get_text(strip=True)
        awayTeam = details.find("span", class_="away_team").get_text(strip=True)
        gameStatus = details.find("span", class_="fixture__number").get_text(strip=True)
        matchDate = '2018' + returnMonth(strMonth) + ordinalDate
        # print (homeTeam, awayTeam, gameStatus, returnCountry(homeTeam), returnCountry(awayTeam), matchDate)
        fixtureSQL = "SELECT fixture_date, fixture_home_team, fixture_away_team, fixture_processed FROM fixtures WHERE " \
                     "fixture_date = '%s' AND fixture_home_team = %d AND fixture_away_team = %d" % (matchDate, returnCountry(homeTeam), returnCountry(awayTeam))
        cursor.execute(fixtureSQL)
        results = cursor.fetchone()
        if results == None:
            cursor.execute("INSERT INTO fixtures (fixture_date, fixture_processed, fixture_home_team, fixture_away_team, fixture_site) "
                           "VALUES ('%s', 0, %d, %d, '%s')" % (matchDate, returnCountry(homeTeam), returnCountry(awayTeam), location))
            cnx.commit()
        matchStadium = []
        matchDetails = []
        # print (returnDay(dayOfWeek), returnMonth(strMonth), ordinalDate, location)
        # print (fixtureSQL)
        # print (i.prettify())

        # print (shr)


    # print (groupTable.prettify())

    #for i in groupRows:
    #    print (i.prettify())
    #    print (shr)
    print ('...')

# print (len(groupContainer))
# Find the Team Groups
groupDivs = scheduleSoup.find_all(id='schedule-by-group')

for i in groupDivs:
    container = i
    div = container.find_all(class_="group-stage gel-layout__item")
    # divA = container.find(id='group-stage--a')
    # print (divA.prettify())
    for i in div:
        teamInsert(i)

# Create BS4 Object from Group Stage
matchRes = requests.get(parseMatch)
matchRes.raise_for_status()
matchSoup = bs4.BeautifulSoup(matchRes.text, "html.parser")

# Parse Stats from Live Match Text
details = matchSoup.find("div", class_='gel-layout')

# print (details.prettify())
rosterRes = requests.get(teamRosters)
rosterRes.raise_for_status()
rosterSoup = bs4.BeautifulSoup(rosterRes.text, "html.parser")

# Begin breakdown to get Rosters by Group and Country
rosterDetails = rosterSoup.find("div", id="responsive-story-page")
rosterDetails = rosterDetails.find("div", id="story-body")
rosterParagraphs = rosterDetails.find_all("p")
# print (rosterDetails.prettify())
print (len(rosterParagraphs[3:]))
print (hr)
rosterCount = 1

def numPos (x):
    playerStr = x
    numPlyrs = playerStr.count(',')+1
    return numPlyrs

def parsePlayers (x):
    rowDetails = x
    # print (rowDetails)
    # numPlyrs = y

    # Regex to parse Players
    pattern = re.compile(r'\,\(?\W*?\,?\W*?\)?')
    matchSplit = re.split('\W*\)?\,', rowDetails)
    outputPlayer = []

    def splitTeam (x):
        if x[0] == ' ':
            playerString = x[1:]
        else:
            playerString = x

        output =[]
        playerTeam = ''
        findPar = playerString.find('(')
        # print (findPar)
        if findPar == -1:
            findPar = len(playerString)
            playerTeam = "NA"
        else:
            playerTeam = playerString[findPar:]
            playerTeam = playerTeam.strip('(,).')

        playerName = playerString[:findPar].rstrip()

        output.append(playerName)
        output.append(playerTeam)
        # print (playerName, playerTeam, findPar)
        return output

    for i in matchSplit:
        player = i
        outputPlayer.append(splitTeam(player))
    # print (outputPlayer)
    return outputPlayer


def parseRoster (x, y):
    rowDetails = x.get_text(strip=True)
    function = y
    outputDetails = []
    # print (rowDetails)
    keeperStart = 12
    defStart = 10
    midStart = 12
    fStart = 9
    # numPos =
    if function == 1:
        countryName = rowDetails
        # print (countryName)
        # 27 23
        prelim = "(final 23 to be confirmed)"
        named = "(final 23 to be named)"
        # Tentative Squad Named
        if prelim in countryName:
            outputDetails.append(countryName[:len(countryName)-27])
            outputDetails.append(0)
            # print (outputDetails)
        # Preliminary Squad Named
        elif named in countryName:
            outputDetails.append(countryName[:len(countryName)-23])
            outputDetails.append(0)
        # Final Squad Named
        else:
            outputDetails.append(countryName)
            outputDetails.append(1)
            # print (outputDetails)
    elif function == 2:
        goalKeepers = rowDetails[keeperStart:]
        outputDetails.append(parsePlayers(goalKeepers))
        # print (outputDetails)
    elif function == 3:
        defenders = rowDetails[defStart:]
        outputDetails.append(parsePlayers(defenders))
        # print (outputDetails)
    elif function == 4:
        midfield = rowDetails[midStart:]
        outputDetails.append(parsePlayers(midfield))
        # print (outputDetails)
    else:
        forwards = rowDetails[fStart:]
        outputDetails.append(parsePlayers(forwards))
        # print(outputDetails)
    return outputDetails

# Create Array to hold Team Data
rosterParse = []

def postRoster (x, y, z):
    players = x
    countryID = y
    pos = z

    cursor = cnx.cursor()
    for i in players:
        # print ("Name", i)
        givenName = i[0]
        givenName = givenName.replace("'", r"\'")
        clubName = i[1]
        clubName = clubName.replace("'", r"\'")
        # print (givenName)
        playerSelect = "SELECT * FROM players WHERE player_givenName = '%s'" % givenName
        cursor.execute(playerSelect)
        results = cursor.fetchone()
        if results == None:
            playerInsert = "INSERT INTO players (player_team_ID, player_givenName, player_clubName, player_Pos) VALUES (%d, '%s', '%s', '%s')" \
                           % (countryID, givenName, clubName, pos)
            cursor.execute(playerInsert)
            cnx.commit()

        # print (givenName, clubName)


cursor = cnx.cursor()
truncStaging = "TRUNCATE TABLE stg_playerdetails"
cursor.execute(truncStaging)
cnx.commit()

for i in rosterParagraphs[2:]:
    # print (i)
    rowParse = i
    rowText = rowParse.get_text(strip=True)
    rowText = rowText.replace("'", r"\'")
    rowText = rowText.replace(",", r"\,")
    rosterParse.append(parseRoster(rowParse, rosterCount))
    # print (rowText)
    cursor = cnx.cursor()

    rosterCount += 1
    insertRawHtml = "INSERT INTO stg_playerDetails (stg_teamID, stg_rowDetails) VALUES (%d, '%s')" % (99, rowText)
    cursor.execute(insertRawHtml)
    cnx.commit()

    if rosterCount > 5:

        rosterCount = 1

        # Update Country on Table
        country = rosterParse[0]
        keepers = rosterParse[1][0]
        defense = rosterParse[2][0]
        midfield = rosterParse[3][0]
        forwards = rosterParse[4][0]

        # Determine if Country Parsed?
        countryName = country[0]
        rosterStatus = country[1]
        countrySql = "SELECT * FROM teams WHERE team_long_name = '%s'" % countryName
        # print (countrySql)
        cursor.execute(countrySql)
        results = cursor.fetchone()
        # print (results)
        countryID = results[0]
        # print (countryID, results[1])
        countryProcessed = results[7]

        if countryID == 999:
            print ('Nigeria... Needs something special')
        elif countryProcessed == 0:
            # Set Country Processed to 1 after processing
            if rosterStatus == 0:
                # print ('To Process Prelim Roster:', results[1])
                # print ('Squad Size GK:',len(keepers), 'DEF: ', len(defense), 'MID:', len(midfield), 'FWD:', len(forwards))
                postRoster(keepers, countryID, 'GK')
                postRoster(defense, countryID, 'DEF')
                postRoster(midfield, countryID, 'MID')
                postRoster(forwards, countryID, 'FWD')
                updateCountry = "UPDATE teams SET team_roster_processed = 2, team_updated = date('%s') WHERE team_ID = %d" % (ds, countryID)
                cursor.execute(updateCountry)
                cnx.commit()
            elif rosterStatus == 1:
                print ('To Process Final Roster:', results[1])
                postRoster(keepers, countryID, 'GK')
                postRoster(defense, countryID, 'DEF')
                postRoster(midfield, countryID, 'MID')
                postRoster(forwards, countryID, 'FWD')
                updateCountry = "UPDATE teams SET team_roster_processed = 1, team_updated = date('%s') WHERE team_ID = %d" % (ds, countryID)
                cursor.execute(updateCountry)
                cnx.commit()
            else:
                print ('Unable to Process', results[1])
        else:
            postRoster(keepers, countryID, 'GK')
            postRoster(defense, countryID, 'DEF')
            postRoster(midfield, countryID, 'MID')
            postRoster(forwards, countryID, 'FWD')
            print ("Already processed", results[1])


        '''
        
        if results == None:
            cursor.execute(
                "INSERT INTO teams (team_short_id, team_long_name, team_badge, team_URL, team_active_ind, team_updated) VALUES (%s, %s, %s, %s, 1, date(%s))",
                (rowAbbr, rowTitle, imgName, urlLink, ds))
            cnx.commit()
            print(rowAbbr, rowTitle)
        '''

        rosterParse = []
        print (hr)

