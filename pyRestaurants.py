#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-12Dec-01
Modified on 2020-01Jan-21
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to parse out Florida Restaurants and Inspections.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2022-10-18       RWM        Initial Stub and Layout
    2022-10-28       RWM        Working Prototype to take active restaurant licenses and
                                inspections and save to MySQL
'''
import os

version = '0.01.a'
# Import Libraries needed for Scraping the various web pages
import datetime
import csv
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
                              host='localhost',
                              database='restaurants',
                              auth_plugin='mysql_native_password')

# Visible Parsing
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Base Path for Output
localPath = 'E:\\OneDrive - Mrga, Inc\\Restaurants_Florida\\'

restaurantFile = 'hrfood1.csv'
inspectionFile = '1fdinspi.csv'

# Change Base Path to localPath
os.chdir(localPath)
print (os.getcwd())

openFile = open(restaurantFile, encoding="utf8")
readRestaurant = csv.reader(openFile)
# restaurantData = list(readRestaurant)
count = 1

for i in readRestaurant:
    break
    # Parse out Row to data fields
    licenceNumber = i[26]
    if len(licenceNumber) > 6:
        shortLicense = licenceNumber[-7:]
    else:
        shortLicense = licenceNumber
    boardCode = i[1]
    licenseName = i[2][:90]
    locationName = i[14][:90]
    locationAddr1 = i[16]
    locationCity = i[19]
    locationZip = i[21]
    locationCountyCd = i[22]
    licenseType = i[1]
    rankCode = i[3]
    numberSeats = i[31]
    if i[29] == '':
        expireDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        expireDate = datetime.datetime.strptime(i[29],'%m/%d/%Y')
    if i[30] != '':
        lastInspection = datetime.datetime.strptime(i[30],'%m/%d/%Y')
    else:
        lastInspection = ''
    print (shortLicense, licenceNumber, rankCode, licenseType, locationName, locationAddr1, locationCity, locationCountyCd, licenseName, numberSeats,  expireDate, lastInspection)
    # print (hr)

    # SQL Inserts and Updates
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute(
        "SELECT LicenseNumber, LicenseExpiry FROM restaurants WHERE LicenseNumber = %s AND LicenseExpiry = %s ",
        (licenceNumber, expireDate))
    results = cursor.fetchone()
    # print (licenseName, expireDate, count)

    if results == None:
        #insert
        # print('Try to add row for %s and the Restaurant Name is %s .' % (licenceNumber, locationName))
        try:
            cursor.execute(
                "INSERT INTO restaurants (LicenseNumber, shortLicenseNumber, ApplicationType, BoardCode, RankCode, LicenseeName, LocationName, LocationAddr1,"
                "LocationCity, LocationZipCode, LocationCountyCd, LicenseExpiry, NumberSeats) "
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (licenceNumber, shortLicense, licenseType, boardCode, rankCode, licenseName, locationName, locationAddr1, locationCity, locationZip,
                 locationCountyCd, expireDate, numberSeats))
            cnx.commit()
            # print('Row added for %s and the Restaurant Name is %s .' % (licenceNumber, locationName))
        except Exception as e:
            print('Row failed to insert for %s and he is %s .' % (licenceNumber, locationName))
            cnx.rollback()

    else:
        print('Row exists for %s and the Restaurant Name is %s.' % (licenceNumber, locationName))
        #
        cursor.execute("UPDATE restaurants SET LicenseeName = %s, LocationName = %s, LocationAddr1 = %s, LocationCity = %s, "
                       "LocationZipCode = %s, LocationCountyCd = %s, LicenseExpiry = %s, NumberSeats = %s "
                       "WHERE LicenseNumber = %s AND LicenseExpiry = %s", (licenseName, locationName, locationAddr1,
                       locationCity, locationZip, locationCountyCd, expireDate, numberSeats, licenceNumber, expireDate))

        cnx.commit()
        #
    count += 1

openFile = open(inspectionFile, encoding="utf8")
readInspections = csv.reader(openFile)
# restaurantData = list(readRestaurant)
count = 1



# Iterate through inspections file
for i in readInspections:
    # print (i)
    inspectionNumber = i[9]
    licenseNumber = i[4]
    inspectionDate = datetime.datetime.strptime(i[14],'%m/%d/%Y')
    inspectionType = i[12]
    inspectionDisposition = i[13]
    totalViolations = i[17]
    violationHighPriority = i[18]
    violationIntermediate = i[19]
    violationBasic = i[20]
    boardCode = i[3]
    licenseName = i[5][:90]
    locationName = i[5][:90]
    locationAddr1 = i[6]
    locationCity = i[7]
    locationZip = i[8]
    locationCountyCd = i[1]
    expireDate = datetime.datetime.strptime(i[14], '%m/%d/%Y')
    inspectionID = i[80]
    visitID = i[81]
    visitNumber = i[10]
    if i[30] != '':
        lastInspection = datetime.datetime.strptime(i[14], '%m/%d/%Y')
    else:
        lastInspection = ''
    if totalViolations == '':
        totalViolations = 0
    if violationHighPriority == '':
        violationHighPriority = 0
    if violationIntermediate == '':
        violationIntermediate = 0
    if violationBasic == '':
        violationBasic = 0

    # print (inspectionNumber, locationName, licenseNumber, inspectionDate, inspectionType, totalViolations, inspectionID, visitID)
    print (inspectionID, visitID, restaurantFile)
#
    # SQL Inserts and Updates
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute(
        "SELECT inspectionNumber, inspectionDate FROM inspections WHERE inspectionNumber = %s AND inspectionDate = %s ",
        (inspectionNumber, inspectionDate))
    results = cursor.fetchone()

    cursor.execute("SELECT shortLicenseNumber from restaurants WHERE shortLicenseNumber = %s" % licenseNumber)
    restaurantExists = cursor.fetchone()

    if restaurantExists == None:
        print ('Adding restaurant', licenseNumber, locationName, restaurantFile)
        try:
            cursor.execute("INSERT INTO restaurants (licenseNumber, shortLicenseNumber, locationName, locationAddr1, locationCity, "
                           "locationCountyCd, LicenseExpiry, LastInspeciton, boardCode, applicationType, licenseeName) "
                       "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (licenseNumber, licenseNumber, locationName, locationAddr1, locationCity, locationCountyCd, expireDate,
                            lastInspection, boardCode, boardCode, locationName))
            cnx.commit()
        except Exception as e:
            print ('Unable to add row for Restaurant %s' % (locationName))
    else:

        cursor.execute ("UPDATE inspections SET inspectionID = %s, visitNumber = %s, visitID = %s "
                        "WHERE inspectionNumber = %s AND inspectionDate = %s",
                        (inspectionID, visitNumber, inspectionNumber, visitID, inspectionDate))
        # print ('Updated Inspection for %s' % locationName)
        cnx.commit()

    if results == None:
        # insert
        # print('Try to add row for %s and the Restaurant Name is %s .' % (licenseNumber, inspectionNumber))

        # try:
        cursor.execute("INSERT INTO inspections (inspectionNumber, LicenseNumber, inspectionDate, inspectionType, inspectionDisposition,"
            "totalViolations, violationHighPriority, violationIntermediate, violationBasic, visitID, inspectionID, visitNumber) "
            "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (inspectionNumber, licenseNumber, inspectionDate, inspectionType, inspectionDisposition, totalViolations,
             violationHighPriority, violationIntermediate, violationBasic, visitID, inspectionID, visitNumber))
        cnx.commit()
            # print('Row added for %s and the Inspection # is %s .' % (licenseNumber, inspectionNumber))
        # except Exception as e:
            # print('Row failed to insert for %s and the Inspeciton # is %s .' % (licenseNumber, inspectionNumber))
            # cnx.rollback()

    else:
        # print('Row exists for %s and the Inspection # is %s.' % (licenseNumber, inspectionNumber))
        cursor.execute("UPDATE inspections SET inspectionID = %s, visitNumber = %s, visitID = %s "
                       "WHERE inspectionNumber = %s AND inspectionDate = %s and visitNumber = %s",
                       (inspectionID, visitNumber, inspectionNumber, visitID, inspectionDate, visitNumber))
        print ('Updated Inspection for %s' % locationName)
        cnx.commit()

        '''
        cursor.execute("UPDATE stg_player_news SET player_news_status = 1, player_rowadded = %s "
                       "WHERE player_firstname = %s AND player_name = %s AND player_team = %s AND seasonID = %s",
                       (updateTS(), playerFirstName, playerName, playerTeam, seasonID))
        cnx.commit()
        '''
    count += 1


    # print (hr)

# Commit and Close the Database Connection.
cnx.commit()
cnx.close()
print('MySQL Connection Closed')