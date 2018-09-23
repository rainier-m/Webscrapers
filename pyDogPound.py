#!python3
# -*- coding: utf-8 -*-
'''
Created on June 12, 2018
Modified on July 14, 2018
Version 0.01.d
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the Miami Dade Animal Services Website
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2018-06Jun-12    RWM        Initial stub and build out of web scraper
    2018-07Jul-14    RWM        Parsing cats and dogs from the Miami Dade Animal Shelter

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
from PIL import Image
import time

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

# Visual Separators for Output
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'Animal Shelter Web Parser v0.01.d'
print(ds + ' :: ' + ts + ' :: ' + parseVersion)
print('Python Version :: ' + sys.version)
print(hr)

# Establish MySQL Connection
cnx = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1',
                              database='dogpound',
                              use_pure=False)

# Setup default web URLs for scraping
baseDogPound = 'http://petharbor.com/results.asp?searchtype=ADOPT&start=3&friends=0&samaritans=0&nosuccess=0&rows=25&imght=300&imgres=detail&tWidth=200&view=sysadm.v_miad&text=000000&fontface=arial&fontsize=10&col_bg=99b5c9&col_bg2=e7eec4&SBG=026BA9&zip=33183&miles=10&shelterlist=%27MIAD%27&atype=&where=type_'
pageNo = 1
maxPageNo = 99
getDogs = 'DOG&'
getCats = 'CAT&'
basePageNo = 'PAGE=1'
pageTxt = 'PAGE='
baseURL = 'http://petharbor.com/'

# Base Path for Output
localPath = 'D:\\DogPound\\'
# localimgPath = 'D:\\DogPound\\img\\'
localimgPath = 'D:\\xampp\\htdocs\\furever\\img\\pets\\'

# Download Images from a passed image URL, give a local filename + extension
def downloadImage(imageURL, localFileName):
    # print (localimgPath + localFileName)
    if os.path.isfile(localimgPath + localFileName) != True:
        response = requests.get(imageURL)
        if response.status_code == 200:
            print('Downloading %s...' % (localFileName))
        with open(localimgPath + localFileName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)
    return True

def num_groups(regex):
    return re.compile(regex).groups

def parsePetRow (x, y):
    # Identify what type of pets to scrape for 1 = Dog, 0 = Cats
    petType = y
    dataRow = x
    cursor = cnx.cursor()
    cellContent = dataRow.find_all('td')
    # print (dataRow.prettify())
    # petPhoto = dataRow.find('a')
    petName = cellContent[1]
    petDesc = cellContent[2]
    petDate = cellContent[3]

    # Get Pet Name & Case Number
    petFullName = petName.get_text()
    petIdStart = petFullName.find("(")
    petName = petFullName[:petIdStart].title()
    petId = petFullName[petIdStart+1:len(petFullName)-1]

    # Get Pet Photo
    photoURL = baseURL + 'get_image.asp?RES=Detail&ID=' + petId + '&LOCATION=MIAD'
    downloadImage(photoURL, petId + '.jpg')

    # Get Pet Shelter Date
    petFullDate = petDate.get_text(strip=True)
    year = petFullDate[:4]
    month = petFullDate[5:7]
    day = petFullDate[8:]
    poundDate = (year + '-' + month + '-' + day)

    # Get Pet Description
    petFullDesc = petDesc.get_text().replace('/', '')
    petFullDesc = petFullDesc.replace('-', '')
    petFullDesc = petFullDesc.replace('(Parson) ', '')
    # print (petFullDesc)

    # Separate the Full Description into components
    wordRegex = re.compile(r"((\w*\s+\w*){1,}\.)")
    sep = wordRegex.findall(petFullDesc)
    # print (sep)
    breed = sep[0][0]
    size = sep[1][0]
    # print (len(sep))
    if len(sep) != 3:
        status = ''
    else:
        status = sep[2][0]

    listBreeds = ['mix', 'Maltese', 'Miniature Pincher', 'Chihuahua', 'Poodle', 'Shih Tzu', 'Dachshund','Weimaraner',
                  'Boxer', 'American Bulldog', 'English Bulldog', 'Bulldog', 'Pit Bull Terrier', 'Mastiff', 'Presa Canario',
                  'Australian Kelpie', 'Beagle', 'Golden Retriever', 'Labrador Retriever', 'German Shepherd', 'Australian Shepherd',
                  'Plott Hound', 'Rottweiler', 'Pointer', 'English Shepherd', 'Tosa', 'Chinese Sharpie', 'Chow Chow', 'Welsh Springer Spaniel',
                  'Terrier', 'Cocker Spaniel', 'Schnauzer', 'Siberian Husky', 'Shiba Inu', 'Dogo Argentino', 'Yorkshire Terrier', 'Boston Terrier',
                  'Dutch Sheepdog', 'Bull Terrier', 'Newfoundland', 'Black Mouth Cur', 'Brasileiro', 'Belgian Malinois', 'Domestic Shorthair',
                  'Domestic Mediumhair', 'Siamese', 'Domestic Longhair','Alaskan Husky','Doberman Pinscher', 'Havanese', 'Pomeranian',
                  'Rat Terrier', 'Lhasa Apso', 'English Bulldog', 'Flat Coated Retriever', 'Papillon', 'Basenji', 'Akita', 'Pug',
                  'American Eskimo', 'Bichon Frise', 'Jack Russell Terrier', 'Border Collie','Whippet', 'Cairn Terrier', 'Pekingese',
                  'Grand Basset Griffon Vendeen', 'Coonhound', 'Basset Hound', 'Bombay', 'Australian Cattle Dog', 'Scottish Fold',
                  'German Pinscher', 'Dutch Shepherd', 'Catahoula Leopard Hound', 'FlatCoated Retriever', 'Bearded Collie', 'St Bernard',
                  'Brussels Griffon', 'Shetland Sheepdog', 'Alaskan Malamute', 'Corgi', 'Welsh Corgi    ', 'Cane Corso', 'Vizsla', 'Dutch Sheepdog']


    foundBreeds = []
    countBreed = 0
    for i in listBreeds:
        toFind = i
        findRegex = re.compile(toFind)
        breedFind = findRegex.search(breed)
        if breedFind != None:
            foundBreeds.append(toFind)
            # print (toFind)

    print (breed)
    breedRegex = re.compile(r"((mix)|"
                            r"(((Maltese)|(Miniature Pinscher)|(Chihuahua)|(Poodle)|(Shih Tzu)|(Dachshund)|(Weimaraner)|(Alaskan Husky))|"
                            r"((Boxer)|(American Bulldog)|(Bulldog)|(Mastiff)|(Presa Canario)|(Australian Kelpie)|(Flat Coated Retriever))|"
                            r"((Beagle)|(Golden Retriever)|(Labrador Retriever)|(Coonhound)|(German Shepherd)|(Australian Shepherd)|"
                            r" (Plott Hound)|(Rottweiler)|(Pointer)|(English Shepherd)|(Tosa)|(Chinese Sharpei)|(Bombay)|(Chow Chow))|"
                            r"((Welsh Springer Spaniel)|(Terrier)|(Schnauzer)|(Cocker Spaniel)|(Spaniel)|(Siberian Husky)|(Shiba Inu))|"
                            r" (Dogo Argentino)|(Yorkshire Terrier)|(Pitt Bull Terrier)|(English Bulldog)|(Boston Terrier)"
                            r" (Dutch Sheepdog)|(Bull Terrier)|(Newfoundland)|(Black Mouth Cur)|(Brasileiro)|(Belgian Malinois)|"
                            r" (Doberman Pinscher)|(Havanese)|(Alaskan Husky)|(Pomeranian)|(Rat Terrier)|(Lhasa Apso)|(Papillon)|"
                            r" (Flat Coated Retriever)|(Basenji)|(Akita)|(American Eskimo)|(Bichon Frise)|(Border Collie)|"
                            r" (Jack Russell Terrier)|(Basset Hound)|(Cairn Terrier)|(Pekingese)|(Grand Basset Griffon Vendeen))|"
                            r"((Domestic Shorthair)|(Domestic Mediumhair)|(Siamese)|(Domestic Longhair)|(Whippet)|(Pug)|"
                            r"(Australian Cattle Dog)|(Scottish Fold)|(German Pinscher)|(Dutch Shepherd)|(Bearded Collie)|"
                            r"(FlatCoated Retriever)|(Catahoula Leopard Hound)|(St Bernard)|(Brussels Griffon)|(Shetland Sheepdog)|"
                            r"(Alaskan Malamute)|(Corgi)|(Cane Corso)|(Welsh Corgi)|(Vizsla)|(Dutch Sheepdog)))")
    breedType = breedRegex.search(breed)
    breedDesc = "Unknown"
    mixRegex = re.compile(r"(mix)")
    mixSearch = mixRegex.search(breed)

    petBreedMix = 0
    if mixSearch != None:
        petBreedMix = 1

    if breedType != None:
        # print (len(breedType.groups()))
        breedDesc = breedType.group(0)
        # print (petName, breedDesc)
        # print (breedType.groups())
    else:
        print("No Breed Found", breed)

    # Get Gender, Determine Intact or Fixed, and Get Description
    gender = ''
    intact = ''
    spay = re.compile(r"(spayed)+")
    neuter = re.compile(r"(neutered)+")
    female = re.compile(r"(female)+")
    male = re.compile(r"(male)+")
    if female.search(breed) != None:
        gender = 'F'
    elif male.search(breed) != None:
        gender = "M"
    else:
        gender = "X"

    if (spay.search(breed) != None) or (neuter.search(breed) != None):
        intact = 'N'
    else:
        intact = 'Y'

    findDesc = breed.find('male')
    desc = breed[findDesc+5:len(breed)-1].title()

    # Get Dog Age and Weight
    # print (size)
    ageRegex = re.compile(r"((\d+ years old)|(\d+\ year and )|(\d+ months )|(\d year old)|(\d+ weeks )|(\d+ days))")
    wgtRegex = re.compile(r"(\d+\s\pounds)")
    ageFind = ageRegex.search(size)
    age = 0
    # print (ageFind.groups())
    # print (age, len(age), age[0][0], age[0][5])
    # print (ageFind.group(0), len(ageFind.group(0)))
    ageText = ageFind.group(0)
    # print(ageFind.group(4), ageFind.groups())

    if len(ageText) == 12:
        age = int(ageText[0:2])
        # print (age)
    elif len(ageText) == 11:
        age = int(ageText[:1])
        # print (age)
    elif ageFind.group(4) != None:
        # print ('Almost a year old...')
        age = 1
    else:
        age = 0

    # print (age)
    wgt = wgtRegex.findall(size)
    # print (wgt)
    if len(wgt) == 0:
        wgt = 0
    else:
        wgt = wgt[0]
        wgt = wgt[0:len(wgt)-7]
        wgt = int(wgt)
    # print (wgt)

    # Get Dog Status
    # print (status)

    # Regex to determine status and condition
    conditionRegex = re.compile(r"(found as a stray)|(turned in by my owner)|(confiscated)")
    condition = conditionRegex.search(status)
    circumstance = 'X'
    # print (condition.groups(), condition.group(0))

    if condition.group(0) == "found as a stray":
        circumstance = '1'
    elif condition.group(0) == "turned in by my owner":
        circumstance = '2'
    else:
        circumstance = '3'

    availRegex = re.compile(r"(may be available for adoption on \d\d \d\d \d\d\d\d)|(am available for adoption)|(may be available for adoption)")
    available = availRegex.search(status)
    petStatus = 'X'

    # print (available.group(0))

    if available.group(0) == "am available for adoption":
        petStatus = 'Y'
    elif available.group(0) == "may be available for adoption":
        petStatus = 'M'
    else:
        petStatus = 'T'
    # print (petStatus)

    # Get Pet Coloring
    # Refactor with a Loop that appends to an array
    # Loop through each color against the Breed and Append Colors found
    ''' Sample Color Patterns
        Black, Black Brindle, Blue, Brown, Brown Brindle, Brown Tiger, Chocolate, Chocolate Point, Cream, Cream Tiger,
        Fawn, Gold, Gray, Gray Tiger, Red, Sable, Silver, Tan, Tricolor, White, Yellow, Yellow Brindle
    '''
    possibleColors = ['black', 'black brindle', 'blue', 'brown', 'brown merle', 'brown brindle', 'brown tiger', 'chocolate', 'chocolate point', 'cream', 'cream tiger',
                      'fawn', 'gold', 'gray', 'gray tiger', ' red', 'sable', 'silver', 'tan', 'tricolor', 'white', 'yellow', 'yellow brindle', 'brown tabby',
                      'calico', 'orange tabby', 'tortie', 'lilac point', 'seal point', 'orange', 'buff']
    foundColors = []
    countColor = 0
    for i in possibleColors:
        toFind = i
        # print (toFind)
        colorRegex = re.compile(toFind)
        colorFind = colorRegex.search(breed)
        if colorFind != None:
            foundColors.append(i)
        # print (foundColors)

    # Clean up foundColors for duplicates of brown/black/chocolate/cream/yellow
    dupColors = ['black brindle', 'brown brindle', 'brown tiger', 'chocolate point', 'cream tiger', 'gray tiger', 'yellow brindle', 'brown tabby']
    for i in foundColors:
        # print (foundColors)
        if i == 'black brindle':
            foundColors.remove('black')
        elif i == 'brown brindle' or i == 'brown tiger' or i == 'brown tabby' or i == 'brown merle':
            foundColors.remove('brown')
        elif i == 'chocolate point':
            foundColors.remove('chocolate')
        elif i == 'cream tiger':
            foundColors.remove('cream')
        elif i == 'gray tiger':
            foundColors.remove('gray')
        elif i == 'yellow brindle':
            foundColors.remove('yellow')

    # print (petId, foundColors)
    for i in foundColors:
        checkPetColorSQL = "SELECT caseNo, color FROM coloring WHERE caseNo = '%s' AND color = '%s'" % (petId, i)
        cursor.execute(checkPetColorSQL)
        colorResults = cursor.fetchone()
        if colorResults == None:
            insertColorSQL = "INSERT INTO coloring (caseNo, color) VALUES ('%s', '%s')" % (petId, i)
            # print (insertColorSQL)
            cursor.execute(insertColorSQL)
            cnx.commit()
    # print (petName, len(foundColors))
    petColor = ''
    if len(foundColors) == 1:
        petColor = foundColors[0]
    elif len(foundColors) == 2:
        petColor = foundColors[0] + ' and ' + foundColors [1]
    elif len(foundColors) == 3:
        petColor = foundColors[0] + ' ' + foundColors[1] + ' and ' + foundColors[2]
    elif len(foundColors) == 4:
        petColor = foundColors[0] + ' ' + foundColors[1] + ' ' + foundColors[2] + ' and ' + foundColors[3]

    # print (breed)

    # Check for the Pet and then update the relevant tables
    checkPetSQL = "SELECT petID from pets WHERE petCaseNo = '%s'" % petId
    cursor.execute(checkPetSQL)
    results = cursor.fetchone()
    if results == None:
        insertPetSQL = "INSERT INTO pets (petActiveInd, petName, petCaseNo, petBreed, petGender, petShelterDate, petAge, petWeight, petIntact, " \
                       "petCircumstance, petAvailable, petModifiedDate, petBreedMix, petType, petColoring, petBreedDesc) " \
                       "VALUES (1, '%s', '%s', '%s', '%s', '%s', %d, %d, '%s', '%s', '%s', '%s', %d, %d, '%s', '%s')" \
                       % (petName, petId, desc, gender, poundDate, age, wgt, intact, circumstance, petStatus, ds, petBreedMix, petType, petColor, breedDesc)
        # print (insertPetSQL)
        cursor.execute(insertPetSQL)
        # print('Added:', petId, petName, desc)
        cnx.commit()
    # Stub out an Elif for updating inactive Rows
    else:
        updatePetSQL = "UPDATE pets SET petModifiedDate = '%s', petAge = %d, petWeight = %d, petBreed = '%s', petIntact = '%s', " \
                       "petCircumstance = '%s', petAvailable = '%s', petBreedDesc = '%s', petBreedMix = %d, petColoring = '%s', petActiveInd = 1" \
                       " WHERE petCaseNo = '%s'" \
                       % (ds, age, wgt, desc, intact, circumstance, petStatus, breedDesc, petBreedMix, petColor, petId)
        # print (breedDesc)
        cursor.execute(updatePetSQL)
        cnx.commit()

    # Clean up multiple instances of Bulldog and Terrier
    for i in foundBreeds:
        # DO SOMETHING
        if i == 'American Bulldog':
            foundBreeds.remove('Bulldog')
        elif i == 'Pit Bull Terrier':
            foundBreeds.remove('Terrier')
            foundBreeds.remove('Bull Terrier')
        elif i == 'Bull Terrier':
            foundBreeds.remove('Terrier')
        elif i == 'Yorkshire Terrier':
            foundBreeds.remove('Terrier')
        elif i == 'Boston Terrier':
            foundBreeds.remove('Terrier')
        elif i == 'Jack Russell Terrier':
            foundBreeds.remove('Terrier')
        elif i == 'Cairn Terrier':
            foundBreeds.remove('Terrier')



    for i in foundBreeds:
        toFind = i
        checkBreedSQL = "SELECT caseNo, petBreedDesc FROM petbreed WHERE caseNo = '%s' and petBreedDesc = '%s'" % (petId, toFind)
        # print (checkBreedSQL)
        cursor.execute(checkBreedSQL)
        breedResults = cursor.fetchone()
        if breedResults == None:
            insertBreedSQL = "INSERT INTO petbreed (caseNo, petBreedDesc) VALUES ('%s', '%s')" % (petId, toFind)
            cursor.execute(insertBreedSQL)
            cnx.commit()

        # print (petName, petId, desc, gender, poundDate, age, wgt)
        # print(petName, petId, breedDesc, desc, gender, poundDate, age, wgt)
        # print ('Updated existing:', petName)
    # print (shr)
    return petId

# cnx.close()

counter = 1
petIds = []
# numPages = 16
while counter <= maxPageNo:
    # Parse each Page
    newURL = baseDogPound + getDogs + pageTxt + str(counter)
    # print (newURL)
    petsAvailable = requests.get(newURL)
    petsAvailable.raise_for_status()
    petSoup = bs4.BeautifulSoup(petsAvailable.text, "html5lib")
    petFoundregex = re.compile(r"(We found \d+ matches)")
    petFound = petFoundregex.search(petSoup.get_text())
    # print (petFound.group(0) )
    if len(petFound.group(0)) == 20:
        petsNum = petFound.group(0)
        petsNum = int(petsNum[9:12])
        maxPageNo = petsNum // 25
        # print (pages, petsNum)

    # with open(os.path.join(localPath + ds + '_' + str(counter) + '.txt'), 'wb') as fo:
    #    for chunk in petsAvailable.iter_content(100000):
    #        fo.write(chunk)

    # Parse out Each Page
    petResults = petSoup.find('table', class_='ResultsTable')
    # print (petResults.prettify())
    petRow = petResults.find_all('tr')
    for i in petRow[1:]:

        # time.sleep(1)
        petIds.append(parsePetRow(i, 1))

    print (hr)

    counter += 1

# Check if Case Number Previously Added
for i in petIds:
    caseNo = i
    checkPetSQL = "SELECT petCaseNumber, CaseNoModified from petCaseNumbers WHERE petCaseNumber = '%s'" % caseNo
    cursor = cnx.cursor()
    cursor.execute(checkPetSQL)
    results = cursor.fetchone()

    # See if the Results need to be created or updated.
    if results == None:
        insertCaseNoSQL = "INSERT INTO petCaseNumbers (petCaseNumber, CaseNoAdded, CaseNoModified, ActiveInd) VALUES ('%s', '%s', '%s', 1)" % (caseNo, ds, ds)
        cursor.execute(insertCaseNoSQL)
        cnx.commit()
    elif results[1] != datetime.date.today():
        print ('Modified DS:', caseNo)
        updateCaseNoSQL = "UPDATE petCaseNumbers SET CaseNoModified = '%s', ActiveInd = 0 WHERE petCaseNumber = '%s'" % (ds, caseNo)
        cursor.execute(updateCaseNoSQL)
        cnx.commit()

# print (petIds)
# Find and parse the returned list of adoptable dogs
# print (petSoup.prettify())

# Get the Cats!
counter = 1
maxPageNo = 3
petIds = []

while counter <= maxPageNo:
    # Parse each Page
    newURL = baseDogPound + getCats + pageTxt + str(counter)
    # print (newURL)
    petsAvailable = requests.get(newURL)
    petsAvailable.raise_for_status()
    petSoup = bs4.BeautifulSoup(petsAvailable.text, "html5lib")
    petFoundregex = re.compile(r"(We found \d+ matches)")
    petFound = petFoundregex.search(petSoup.get_text())
    # print (petFound.group(0), )
    if len(petFound.group(0)) == 20:
        petsNum = petFound.group(0)
        petsNum = int(petsNum[9:12])
        maxPageNo = petsNum // 25
        # print (pages, petsNum)

    # with open(os.path.join(localPath + ds + '_' + str(counter) + '.txt'), 'wb') as fo:
    #    for chunk in petsAvailable.iter_content(100000):
    #        fo.write(chunk)

    # Parse out Each Page
    petResults = petSoup.find('table', class_='ResultsTable')
    # print (petResults.prettify())
    petRow = petResults.find_all('tr')
    for i in petRow[1:]:

        # time.sleep(1)
        petIds.append(parsePetRow(i, 0))

    print (hr)

    counter += 1

for i in petIds:
    caseNo = i
    checkPetSQL = "SELECT petCaseNumber, CaseNoModified from petCaseNumbers WHERE petCaseNumber = '%s'" % caseNo
    cursor = cnx.cursor()
    cursor.execute(checkPetSQL)
    results = cursor.fetchone()

    # See if the Results need to be created or updated.
    if results == None:
        insertCaseNoSQL = "INSERT INTO petCaseNumbers (petCaseNumber, CaseNoAdded, CaseNoModified) VALUES ('%s', '%s', '%s')" % (caseNo, ds, ds)
        cursor.execute(insertCaseNoSQL)
        cnx.commit()
    elif results[1] != datetime.date.today():
        print ('Modified DS:', caseNo)
        updateCaseNoSQL = "UPDATE petCaseNumbers SET CaseNoModified = '%s' WHERE petCaseNumber = '%s'" % (ds, caseNo)
        cursor.execute(updateCaseNoSQL)
        cnx.commit()

# Read Image and determine size of images
