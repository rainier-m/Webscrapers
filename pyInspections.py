#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-12Dec-01
Modified on 2020-01Jan-21
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to parse out Florida Inspections.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2022-10-18       RWM        Initial Stub and Layout
    2022-10-28       RWM        Working Prototype to take active restaurant licenses and
                                inspections and save to MySQL
    2024-02-22       RWM        Refactor for new dev on Toolbox server
    2024-02-25       RWM        Refactor to have two functions for Restaurants & Inspections
    2025-02-21       RWM        Fork to just run Inspection Files and not Restaurants.
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

fileNumber = '4'

# Create the File Name for the Restaurants & Inspections
# restaurantFile = 'hrfood'+ fileNumber + '.csv'
inspectionFile = fileNumber + 'fdinspi.csv'

# Change Base Path to localPath
os.chdir(localPath)
print (os.getcwd())

runDate = updateTS()

def count_rows_in_csv(file_path):
    with open(file_path, mode='r', encoding="utf8") as file:
        reader = csv.reader(file)
        row_count = sum(1 for row in reader)  # Count rows
    return row_count

openFile = open(inspectionFile, encoding="utf8")
readInspections = csv.reader(openFile)
next(readInspections)
# restaurantData = list(readRestaurant)
count = 1

rowsInspection = count_rows_in_csv(inspectionFile)

# Iterate through inspections file
for i in readInspections:
    # print (i[14])

    inspectionNumber = i[9]
    licenseNumber = i[4]
    inspectionDate = datetime.datetime.strptime(i[14],'%m/%d/%Y')
    inspectionDate = inspectionDate.strftime("%Y-%m-%d %H:%M:%S")
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
    expireDate = expireDate.strftime("%Y-%m-%d %H:%M:%S")
    inspectionID = i[80]
    visitID = i[81]
    visitNumber = i[10]
    district = fileNumber
    # print (i[14])
    if i[30] != '':
        lastInspection = datetime.datetime.strptime(i[14], '%m/%d/%Y')
        lastInspection = lastInspection.strftime("%Y-%m-%d %H:%M:%S")
    else:
        lastInspection = ''
    # print (lastInspection, type(i[30]), locationName)
    if totalViolations == '':
        totalViolations = 0
    if violationHighPriority == '':
        violationHighPriority = 0
    if violationIntermediate == '':
        violationIntermediate = 0
    if violationBasic == '':
        violationBasic = 0

    # print (inspectionNumber, locationName, licenseNumber, inspectionDate, inspectionType, totalViolations, inspectionID, visitID)
    # print (inspectionID, visitID, restaurantFile)
    # SQL Inserts and Updates
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute(
        "SELECT inspectionNumber, inspectionDate FROM inspections WHERE inspectionNumber = %s AND inspectionDate = %s ",
        (inspectionNumber, inspectionDate))
    results = cursor.fetchone()

    cursor.execute("SELECT shortLicenseNumber from restaurants WHERE shortLicenseNumber = %s" % licenseNumber)
    restaurantExists = cursor.fetchone()

    if restaurantExists == None:
        print ('Adding restaurant', licenseNumber, locationName, inspectionFile)
        inspectionAdd = 1
        try:
            cursor.execute("INSERT INTO restaurants (licenseNumber, shortLicenseNumber, locationName, locationAddr1, locationCity, "
                           "locationCountyCd, runDate, district, inspectionAdd) "
                       "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (licenseNumber, licenseNumber, locationName, locationAddr1, locationCity, locationCountyCd, runDate, district, inspectionAdd))
            cnx.commit()
            # print(licenseNumber, shortLicenseNumber, locationName, locationAddr1, locationCity,locationCountyCd, expireDate, lastInspection, boardCode, applicationType, licenseeName)
            print ('Row added for Restaurant Inspection %s' % locationName)
        except Exception as e:
            print ('Unable to add row for Restaurant %s' % (locationName), lastInspection, e)

    if results == None:
        # insert
        # print('Try to add row for %s and the Restaurant Name is %s .' % (licenseNumber, inspectionNumber))

        # try:
        cursor.execute("INSERT INTO inspections (inspectionNumber, LicenseNumber, inspectionDate, inspectionType, inspectionDisposition,"
            "totalViolations, violationHighPriority, violationIntermediate, violationBasic, visitID, inspectionID, visitNumber, district, runDate) "
            "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (inspectionNumber, licenseNumber, inspectionDate, inspectionType, inspectionDisposition, totalViolations,
             violationHighPriority, violationIntermediate, violationBasic, visitID, inspectionID, visitNumber, district, runDate))
        cnx.commit()
        print('Row added for %s and the Inspection # is %s .' % (licenseNumber, inspectionNumber))
    '''
    else:
        # Fix needed to get Inspection Run Date updated on Inspection Update. Also, possibly remove / skip this section once completed.
        cursor.execute("UPDATE inspections SET runDate = '%s', district = '%s' WHERE inspectionNumber = '%s' AND inspectionDate = '%s'" % (runDate, district, inspectionNumber, inspectionDate))
        print('Updated Inspection for %s' % locationName)
        cnx.commit()

        # except Exception as e:
            # print('Row failed to insert for %s and the Inspeciton # is %s .' % (licenseNumber, inspectionNumber))
            # cnx.rollback()

    else:
        # print('Row exists for %s and the Inspection # is %s.' % (licenseNumber, inspectionNumber))
        cursor.execute("UPDATE inspections SET inspectionID = %s, visitNumber = %s, visitID = %s , runDate = %s"
                       "WHERE inspectionNumber = %s AND inspectionDate = %s and visitNumber = %s",
                       (inspectionID, visitNumber, inspectionNumber, visitID, inspectionDate, visitNumber, runDate))
        print ('Updated Inspection for %s' % locationName)
        cnx.commit()
    '''

    percentComplete = count/(rowsInspection-1)
    print("Processed:","{:.3%}".format(percentComplete),"of Inspections")
    # print("Row", count, "of", rowsInspection, "Processed")
    count += 1
    print (hr)

# Commit and Close the Database Connection.
cnx.commit()
cnx.close()
print('MySQL Connection Closed')

