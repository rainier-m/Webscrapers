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
    2020-05May-14    RWN        Initial Creation of the file to parse out Covid Details to MySQL

'''

# Import Libraries needed for Scraping the various web pages
import re
import datetime
import csv
import os
import sys
import codecs
import mysql.connector

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

# Data Local Path
dataPath = 'E:\\CovidAnalysis\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports_us'
globalPath = 'E:\\CovidAnalysis\\COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports'

def returnInt(input):
    reviewValue = input
    if reviewValue == '':
        return 0
    else:
        return reviewValue


# Parse Global CSV file
for file in os.listdir(globalPath):
    filename = os.path.basename(file)
    if filename[-3:] == 'csv':
        print(filename)
        openFile = open(os.path.join(globalPath + '\\' + filename))
        readFile = csv.reader(openFile)
        dataFile = list(readFile)
        for i in dataFile[1:]:
            # print (i)
            fips = i[0]
            county = i[1]
            provinceState = i[2]
            countryRegion = i[3]
            lastUpdated = filename[6:-4] + '-' + filename[0:2] + '-' + filename[3:5]
            lat = i[5]
            if i[6] is None:
                long = 0
            else:
                long = i[6]
            confirmed = returnInt(i[7])
            deaths = returnInt(i[8])
            recovered = returnInt(i[9])
            active = returnInt(i[10])
            combineKey = i[11]
            cursor = cnx.cursor()

            try:
                cursor.execute("INSERT INTO `covid_db`.`covid_daily` (`fips`, `county`, `provinceState`, `countryRegion`, "
                               "`lastUpdated`, `lat`, `long`, `confirmed`, `deaths`, `recovered`, `active`, `combinedKey`)"
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fips, county, provinceState,
                                                                                           countryRegion, lastUpdated, lat,
                                                                                           long, confirmed, deaths, recovered,
                                                                                           active, combineKey))
                print ('Row successfully added for %s %s on the %s' % (provinceState, countryRegion, lastUpdated))
                cnx.commit()

            except Exception as e:
                print('Row failed to update for %s on the %s.' % (countryRegion, lastUpdated))
                cnx.rollback()

# Parse US CSV File
for file in os.listdir(dataPath):
    filename = os.path.basename(file)
    if filename[-3:] == 'csv':
        print (filename)
        openFile = open(os.path.join(dataPath + '\\' + filename))
        readFile = csv.reader(openFile)
        dataFile = list(readFile)
        for i in dataFile[1:]:
            # print (i)
            state = i[0]
            countryRegion = i[1]
            lastUpdated = filename[6:-4] + '-' + filename[0:2] + '-' + filename[3:5]
            # print(lastUpdated)
            recovered = returnInt(i[7])
            hospitalized = returnInt(i[12])
            hospitalRate = returnInt(i[17])
            incidentRate = returnInt(i[10])
            peopleTested = returnInt(i[11])
            testingRate = returnInt(i[16])
            mortality = returnInt(i[13])
            active = returnInt(i[8])

            # 18 sets in list
            cursor = cnx.cursor()

            try:
                cursor.execute("INSERT INTO `covid_db`.`covid_us_daily` (`province_state`, `country_region`, `lastUpdated`, `lat`, `long`, `Confirmed`, `Deaths`,"
                           "`Recovered`,`Active`,`FIPS`,`IncidentRate`,`PeopleTested`,`PeopleHospitalized`,`MortalityRate`,`UID`,`ISO3`,`TestingRate`,`HospitalRate`) "
                           "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (state, countryRegion, lastUpdated, 0, 0,
                                                                                                              i[5], i[6], recovered, active, i[9], incidentRate,
                                                                                                              peopleTested, hospitalized, mortality, i[14], i[15],
                                                                                                              testingRate, hospitalRate))
                    # "UPDATE stg_player_news SET player_news_status = 1, player_rowadded = %s "
                    #           "WHERE player_firstname = %s AND player_name = %s AND player_team = %s AND seasonID = %s",
                    #           (updateTS(), playerFirstName, playerName, playerTeam, seasonID))
                cnx.commit()
                # print(updateTS(), playerFirstName, playerName, playerTeam, seasonID)
                # print('Row exists for %s and he is %s.' % (playerName, playerStatus))
            except Exception as e:
                print('Row failed to update for %s on the %s.' % (i[0], i[2]))
                cnx.rollback()
            # '''
        print (shr)
    else:
        print ('Not a CSV File')

# Commit and Close the Database Connection.
cnx.commit()
cnx.close()
print('MySQL Connection Closed')