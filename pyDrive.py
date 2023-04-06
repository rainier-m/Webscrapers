#!python3
# -*- coding: utf-8 -*-
'''
Created on Sep 07, 2022
Modified on Sep 07, 2022
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the contents of my Google Drive and catalogue it
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2022-09Sep-07    RWN        Initial Creation of this Python script
'''

# Import necessary Libraries
import os
import datetime
import sys
import codecs
import pandas as pd
import math
from PyPDF2 import PdfReader


# Provide Google Drive Physical Location
drive_loc = 'G:\\Games\\'

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

# Create Pandas dataframe for Google Drive inventory
pd.set_option("display.max_rows", None, "display.max_columns", None)

hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

print (os.listdir(drive_loc))

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

# Iterate over the contents of Google Drive
'''
for folderName, subfolders, filenames in os.walk(drive_loc):
    print ('The current Folder is: ', folderName)
    print (hr)
    for subfolder in subfolders:
        print ('Subfolder of', folderName, 'is :', subfolder)
        print (shr, 'Subfolder Start')

        for filename in filenames:
            print ('Files inside', folderName, ':', filename)
        print (shr)
'''

# Dataframe creation
df = pd.DataFrame(columns=['ID', 'Directory', 'File Name', 'File Extension', 'File Size', 'Page Number'])

count = 0

for root, dirs, files in os.walk(drive_loc, topdown = False):
    for name in files:
        filesizeBytes = os.path.getsize(os.path.join(root, name))
        filesizeStr = convert_size(filesizeBytes)
        splitFileExtension = os.path.splitext(os.path.join(root, name))
        fileName = splitFileExtension[0]
        fileExtension = splitFileExtension[1][1:]
        pageCount = 0
        count += 1
        list_row = [count, root, name, fileExtension, filesizeStr, pageCount]
        df.loc[len(df)] = list_row
        print(count, ':', root, ':', name, ':', fileExtension, ':', filesizeStr)

# print (df)
df.to_csv('~/Desktop/gamesInventory.csv', sep='|')
print (os.getcwd())
