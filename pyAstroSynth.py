#!python3
# -*- coding: utf-8 -*-
'''
Created  Jan 29, 2018
Modified Jan 29, 2018
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the AstroSynthesis HTML file for content.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2016-01Jan-15    RWN        Initial Creation of the file
'''
# Import Libraries needed for Scraping the various web pages
import bs4
import xml.etree.ElementTree as etree
import datetime
import openpyxl
import os
import sys
import mysql.connector

print('Python Version :: ' + sys.version)

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Output Strings
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Base Path for Input
localPath = 'H:\\Games\\Fading Suns\\'
localURL  = 'file://H:/Games/Fading%20Suns/'
localFile = 'KnownUniverse.xml'

# Base Path for Output
baseWkBk = "Book1.xlsx"
workbook = openpyxl.load_workbook(os.path.join(localPath + baseWkBk))

# Base Path for HTML
systems = etree.parse(os.path.join(localPath + localFile))
root = systems.getroot()




# print (sysSoup.prettify())
