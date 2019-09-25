#!python3
# -*- coding: utf-8 -*-
'''
Created on  June 18, 2019
Modified on June 18 , 2019
Version 0.01.a
@author: rmadruga@nclcorp.com
A simple Python Program to randomly generate Publix subs
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
   2019-06Jun-18    RWM        Initial stub and build out
'''

import datetime
import random
import html
import os
import openpyxl
import sys

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H%M%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

print('Python Version :: ' + sys.version)

# Output Dividers
hr = " >>> *** ====================================================== *** <<<"
shr = " >>> *** ==================== *** <<<"

# Updates the Time Stamp
def updateTS():
   update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   return update

# Base Path for Output
localPath = 'F://Projects//Python//'

# Sub Details
subType = ['Bourbon Ridge Ham', 'Turkey', 'Ultimate', 'Italian', 'Chicken Tender', 'Roast Beef', 'Havana Bold', 'Chicken Cordon Bleu',
          'Ham', 'Deluxe', 'Philly Cheese', 'American', 'Rueben - Corned Beef', 'Maple Honey Turkey', 'EverRoast', 'Jerk Turkey',
          'Veggie', 'Tuna Salad', 'Egg Salad', 'Cuban Sub', 'Mojo Pork', 'Ham & Turkey', 'Chicken Salad', 'Beef Meatball']
bread = ['Italian 5 Grain', 'White', 'Whole Wheat', 'Flatbread', 'Rye', 'Cuban Bread', 'Ciabatta', 'Salad']
cheese = ['Cheddar', 'Muenster', 'Provolone', 'Swiss', 'White American', 'Yellow American', 'Gouda','No Cheese']
extras = ['Double Meats', 'Double Cheese', 'Bacon', 'Guacamole', 'Hummus', 'Black Bean Hummus']
toppings = ['Banana Peppers', 'Black Olives', 'Garlic Pickles', 'Cucumber', 'Dill Pickles', 'Green Peppers', 'Jalapeno Peppers',
           'Lettuce', 'Onions', 'Spinach', 'Tomato', 'Salt', 'Black Pepper', 'Oregano', 'Oil', 'Vinegar', 'Sauerkraut']
condiments = ['Honey Mustard', 'Spicy Mustard', 'Mayonnaise', 'Yellow Mustard', 'Thousand Islands Dressing']
heating = ['Pressed', 'Toasted', 'None']

counter = 1

subs = []

possibleSubs = {}

while counter <= 10:
   randSub = random.choice(subType)
   randBread = random.choice(bread)
   randCheese = random.choice(cheese)

   possibleSubs[counter] = {'subDetails' : {'subType' : randSub, 'bread' : randBread, 'randCheese' : randCheese }}
   #print(possibleSubs)

   # subs.append(randSub, randBread, randCheese)

   def reqExtras(s, c):
       numExtras = random.randint(0,len(extras)+1)
       subCon = s
       cheeseCon = c
       extraCount = 1
       subExtras = []
       # print (numExtras)
       modExtras = extras
       extraString = ''
       # print (s, c)

       if numExtras == 0:
           extraString = '  no extras'
       while extraCount <= numExtras:
           randExtras = random.choice(modExtras)
           subExtras.append(randExtras)
           extraCount += 1
       subExtras = list(dict.fromkeys(subExtras))
       if subCon == 'Veggies' and 'Double Meats' in subExtras:
           subExtras.remove('Double Meats')
       if cheeseCon == 'No Cheese' and 'Double Cheese' in subExtras:
           # numExtras = 0
           subExtras.remove('Double Cheese')
           # print (randExtras)

       subExtras.sort()

       if len(subExtras) == 0:
           extraString = '  no extras'
       for i in subExtras:
           extraString = extraString + ', ' + i
       return extraString[2:]

   def reqToppings():
       numToppings = random.randint(1,len(toppings))
       # print(numToppings)
       topCounter = 1
       subToppings = []
       while topCounter <= numToppings:
           randTopping = random.choice(toppings)
           # print (randTopping)
           subToppings.append(randTopping)
           topCounter += 1
       topString = ''
       subToppings = list(dict.fromkeys(subToppings))
       subToppings.sort()
       # subToppings = subToppings.sort()
       # print(subToppings)
       for i in subToppings:
           topString = topString + ', ' + i
       return topString[2:]

   def reqCondiments():
       numCondiments = random.randint(0, len(condiments))
       condCount = 1
       subCondiments = []
       condString = ''
       if numCondiments == 0:
           condString = '  no condiments'
       while condCount <= numCondiments:
           randCondiment = random.choice(condiments)
           subCondiments.append(randCondiment)
           condCount += 1
       subCondiments = list(dict.fromkeys(subCondiments))
       subCondiments.sort()
       for i in subCondiments:
           condString = condString + ', ' + i
       return condString[2:]

   print ("Sub #:", counter)
   print (randSub, 'on', randBread, 'with', randCheese, '\r\n   with', reqToppings(), '\r\n   and',
          reqExtras(randSub, randCheese), '\r\n   covered with', reqCondiments())
   print (shr)
   extrasRule = extras
   counter += 1
# print (possibleSubs)
# for p_id, subDets in possibleSubs.items():
#     print (subDets)
