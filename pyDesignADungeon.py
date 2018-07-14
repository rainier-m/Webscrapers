#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-11Nov-22
Modified on 2017-11Nov-22
Version 0.01.a
@author: rainier.madruga@gmail.com
### =========================================================================================== ###
    A simple Python Program to randomly generate a Dungeon using
    Tony Dowler's "How to Host a Dungeon"
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2017-11-22       RWM        Initial Stub and Layout
'''

# Import necessary libraries
import random
import datetime

# Visual Spacing Elements for Parsing
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Create Randomized Token
very_random = random.SystemRandom()


# Input for Width and Depth of Map
# mapArray is 12x20 using the following setup:
#       Above Ground are indexes 0 and 1
#       Everything else is Below Ground
mapArray = [[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
            [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
            ]

depth = len(mapArray)
width = len(mapArray[0])
surface = 0

# Describe the mapArray
print ("mapArray is:", str(len(mapArray)), "layers deep.")
print ("mapArray is:", str(len(mapArray[0])), "layers wide")

# Function to roll a number of Dice...
def diceRoll(int1, int2):
    numDice = int1
    numSides = int2
    count = 0
    result = 0
    # print (result)
    # print (numDice, numSides)
    while count < numDice:
        # print (random.randint(1,numSides))
        result = result + random.randint(1,numSides)
        count += 1
        # print (shr, '\n', result, '\n', shr)
    return result


# Build the Map...
# print (str(diceRoll(1,8)))
# print (str(diceRoll(2,8)))

# Print the Map Results
# for i in mapArray:
    # print (i)

def placeMap(event, type):
    placeEvent = event
    placeType = type



# Primordial Age
def numEvents (num, die):
    result = diceRoll(num, die)
    return result



def primordialEvent ():
    event = []
    getEvents = numEvents(2,8)
    count = 0
    while count <= getEvents:
        eventDice = diceRoll(1,8)
        if eventDice == 1:
            event.append("Mithril")
        elif eventDice == 2:
            event.append("Natural Caverns")
        elif eventDice == 3:
            event.append("Natural Caverns")
        elif eventDice == 4:
            event.append("Gold Vein")
        else:
            print ("Dice out of Range", eventDice)

        count += 1
        print (count)
    return event

events = primordialEvent()
print (events)
