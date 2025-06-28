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
    2024-02-22       RWM        Refactor for new dev on Toolbox server
    2024-02-25       RWM        Refactor to have two functions for Restaurants & Inspections
'''
import os

version = '0.01.a'
# Import Libraries needed for Scraping the various web pages
import datetime
import csv
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
                              host='dewalt',
                              database='restaurants',
                              auth_plugin='mysql_native_password')

# Visible Parsing
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Base Path for Output
localPath = 'D:\\OneDrive - Mdga, Inc\\Restaurants_Florida\\'

fileNumber = '1'

restaurantFile = 'hrfood'+ fileNumber + '.csv'
inspectionFile = fileNumber + 'fdinspi.csv'

# Change Base Path to localPath
os.chdir(localPath)
print (os.getcwd())

openFile = open(restaurantFile, encoding="utf8")
readRestaurant = csv.reader(openFile)
next(readRestaurant)
# restaurantData = list(readRestaurant)
count = 1
runDate = updateTS()

def count_rows_in_csv(file_path):
    with open(file_path, mode='r', encoding="utf8") as file:
        reader = csv.reader(file)
        row_count = sum(1 for row in reader)  # Count rows
    return row_count

rowsRestaurant = count_rows_in_csv(restaurantFile)

for i in readRestaurant:
    # Parse out Row to data fields
    licenceNumber = i[27]
    if len(licenceNumber) > 6:
        shortLicense = licenceNumber[-7:]
    else:
        shortLicense = licenceNumber
    boardCode = i[1]
    licenseName = i[2][:90]
    locationName = i[14][:90]
    if locationName == '':
        locationName = licenseName
    locationAddr1 = i[16]
    locationCity = i[19]
    locationZip = i[21]
    locationCountyCd = i[22]
    licenseType = i[1]
    rankCode = i[3]
    numberSeats = i[32]
    district = i[25]
    if district == '':
        district = fileNumber
    # print (district)
    # print (i[30])

    if i[30] != '':
        expireDate = datetime.datetime.strptime(i[30],'%m/%d/%Y')
    if i[31] != '':
        lastInspection = datetime.datetime.strptime(i[31],'%m/%d/%Y')
    else:
        lastInspection = ''
    # print(expireDate)

    if i[32] == '':
        numberSeats = 0
    # print (shortLicense, licenceNumber, rankCode, licenseType, locationName, locationAddr1, locationCity, locationCountyCd, licenseName, numberSeats,  expireDate, lastInspection, district)
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
        # print (numberSeats)
        try:
            cursor.execute(
                "INSERT INTO restaurants (LicenseNumber, shortLicenseNumber, ApplicationType, BoardCode, RankCode, LicenseeName, LocationName, LocationAddr1,LocationCity, LocationZipCode, LocationCountyCd, LicenseExpiry, NumberSeats, runDate, district) "
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (licenceNumber, shortLicense, licenseType, boardCode, rankCode, licenseName, locationName, locationAddr1, locationCity, locationZip,locationCountyCd, expireDate, numberSeats, runDate,district))
            cnx.commit()
            print('Row added for %s and the Restaurant Name is %s .' % (licenceNumber, locationName))
        except Exception as e:
            print('Row failed to insert for %s and he is %s .' % (licenceNumber, locationName), e)
            cursor.execute("INSERT INTO parselog (runDate, logREsult) values (%s, %s)" % (runDate, e))
            cnx.commit()
            cnx.rollback()

    else:
        print('Row exists for %s and the Restaurant Name is %s.' % (licenceNumber, locationName))
        #
        cursor.execute("UPDATE restaurants SET LicenseeName = %s, LocationName = %s, LocationAddr1 = %s, LocationCity = %s, "
                       "LocationZipCode = %s, LocationCountyCd = %s, LicenseExpiry = %s, NumberSeats = %s , runDate = %s, district = %s, runDate =%s, inspectionAdd =%s" 
                       "WHERE LicenseNumber = %s AND LicenseExpiry = %s", (licenseName, locationName, locationAddr1,
                       locationCity, locationZip, locationCountyCd, expireDate, numberSeats, runDate, district, runDate, "0", licenceNumber, expireDate))

        cnx.commit()
        #

    # print ("Row", str(count), "of", str(rowsRestaurant), "Processed")
    percentComplete = count / (rowsRestaurant - 1)
    print("Processed:", "{:.3%}".format(percentComplete), "of Restaurants")
    count += 1

# Commit and Close the Database Connection.
cnx.commit()
cnx.close()
print('MySQL Connection Closed')

