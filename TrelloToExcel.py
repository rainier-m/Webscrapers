#!python3
# -*- coding: utf-8 -*-
'''
Created on Jul 20, 2020
Modified on JUl 20, 2020
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to build Day Trading information for review
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2021-09Sep-20    RWN        Initial Creation of the file to parse JSON from Trello Export

'''

# Import Libraries needed for Scraping the various web pages
import datetime
import os
import sys
import codecs
import json
import openpyxl
import requests

# Set Character Output
print('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

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
localPath = 'E:\\Python\\'
localSavePath = 'E:\\Python\\MiamiDownloads\\'
dataFile = 'E:\\Python\\Permits_Trello.json'
baseWkBk = 'TrelloCards_Template.xlsx'
newWkBk = 'TrelloCards_Permit.xlsx'
workBook = openpyxl.load_workbook(os.path.join(localPath + baseWkBk))
baseSheet = workBook['Sheet1']

# Download Image
def downloadFile(fileURL, localFileName):
    # response =
    with requests.get(fileURL, stream=True) as r:
        r.raise_for_status()
        with open(localSavePath + localFileName, 'wb') as fo:
            for chunk in response.iter_content(8192):
                fo.write(chunk)
    return True

jsonFile = open(dataFile, encoding='utf-8')
jsonFile = json.load(jsonFile)

boardLists = dict()
for item in jsonFile['lists']:
    listID = item['id']
    listName = item['name']
    boardLists[listID] = listName

boardLabels = dict()
for item in jsonFile['labels']:
    labelID = item['id']
    labelName = item['name']
    boardLabels[labelID] = labelName

boardChecklists = dict()
for item in jsonFile['checklists']:
    # print (item)
    listID = item['id']
    listName = item['name']
    listCheckItems = item['checkItems']
    boardChecklists[listID] = listName

def getListItems(listName):
    listItems = dict()
    toProcess = listName
    checkDetails = dict()

    for attrs in jsonFile['checklists']:
        if attrs['id'] == toProcess:
            listItems = {"id": toProcess, "name": attrs['name']}
            for item in attrs['checkItems']:
                itemName = item['name']
                itemState = item['state']
                itemAssigned = item['idMember']
                if itemAssigned is None:
                    itemAssigned = {"idMember" : 'N/A'}
                checkDetails[itemName] = itemState
                # checkDetails.update(itemAssigned)
                # print (item['name'], item['state'])
    # print (listItems)
    # print (checkDetails)
    listItems = listItems | checkDetails
    # print (listItems)
    return listItems

cardCounter = 2

for card in jsonFile['cards']:
    # print (card['name'], '|', card['desc'], '|', card['id'], '|', card['idBoard'], '|', card['idList'])
    # print (card)
    cardList = card['idList']
    cardName = card['name']
    cardActivity = card['dateLastActivity']
    cardListName = boardLists[cardList]
    cardDesc = card['desc']
    cardLabels = card['idLabels']
    cardLabelNames = ''
    cardListItems = card['idChecklists']
    cardCheckList = ''
    cardAttachments = card['attachments']
    cardAttachementsDetails = ''

    for item in cardLabels:
        cardLabelNames = cardLabelNames + boardLabels[item]

    for item in cardListItems:
        # print (item)
        cardItems = getListItems(item)
        for key, item in cardItems.items():
            cardCheckList = cardCheckList +( key + ' | ' + item + ' \n')

    if len(cardAttachments) > 0:
        # print (cardAttachments)
        for file in cardAttachments:
            fileName = file['fileName']
            url = file['url']
            if fileName[len(fileName)-3:].lower() != 'png':
                cardAttachementsDetails = cardAttachementsDetails + fileName + ' \n'
                # print (fileName)
                # downloadFile(url, fileName)

    '''
        if 'idChecklists' in card:
        # print (card['idCheckLists'])
        cardListItems = 'Has Checklist'

    else:
        cardListItems = 'N/A'
        cardCheckListID = boardChecklists[card['idCheckLists']]
        print (cardCheckListID)
    '''
    sheetCard = baseSheet['A'+str(cardCounter)]
    sheetName = baseSheet['B' + str(cardCounter)]
    sheetActivity = baseSheet['C' + str(cardCounter)]
    sheetListName = baseSheet['D' + str(cardCounter)]
    sheetDesc = baseSheet['E' + str(cardCounter)]
    sheetLabels = baseSheet['F' + str(cardCounter)]
    sheetChecklist = baseSheet['G' + str(cardCounter)]
    sheetAttachments = baseSheet['H' + str(cardCounter)]

    sheetCard.value = cardList
    sheetName.value = cardName
    sheetActivity.value = cardActivity[:10]
    sheetListName.value = cardListName
    sheetDesc.value = cardDesc
    sheetLabels.value = cardLabelNames
    sheetChecklist.value = cardCheckList
    sheetAttachments.value = cardAttachementsDetails

    # print (cardName, '|', cardListName, '|', cardActivity[:10], '|', cardLabelNames, '|', cardDesc, '|', cardListItems)
    cardCounter += 1
    # print (shr)
workBook.save(localPath + newWkBk)
