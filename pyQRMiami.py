#!python3
# -*- coding: utf-8 -*-
'''
Created on Oct 25, 2021
Modified on Oct 25, 2021
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to build Day Trading information for review
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2021-10Oct-25    RWN        Initial Creation of the file to grab data and parse as needed

'''

# Import Libraries needed for Scraping the various web pages
import datetime
import string
import random
import sys
import codecs
from google.cloud.sql.connector import connector
from google.cloud import storage
import json

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Establish MySQL Connection
storage_client = storage.Client.from_service_account_json('property-api-330113-3624f00e2c65.json')
buckets = list(storage_client.list_buckets())
# print (buckets)

conn = connector.connect(
    "property-api-330113:us-central1:propertydetails",
    "pymysql",
    user="root",
    password="whBychdmI0Cdh1ux",
    db="property"
    )

cursor = conn.cursor()

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
globalPath = 'Property_Card.json'

# print (os.path.exists(globalPath))
def id_generator(size = 8, chars = string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


with open(globalPath) as data:
    jsonObj = json.load(data)
    # print (jsonObj)

count = 0
parcelFolioCt = 1
for i in jsonObj["features"]:
    # print (i)
    propObjID = i['properties']['OBJECTID']
    propAddress = i['properties']['ADDRESS']
    folio = i['properties']['FOLIO']
    parcelFolio = i['properties']['PARCELFOLIO']
    zipCode = i['properties']['ZIPCODE']
    urlCode = id_generator()
    if folio != parcelFolio:
        print(propObjID, '|', propAddress)
        print (parcelFolioCt)
        print (urlCode)
        parcelFolioCt += 1
        print(shr)

    # print (str(count))
    count += 1
    # print (i)

