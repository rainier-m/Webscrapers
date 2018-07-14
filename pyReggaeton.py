#!python3
# -*- coding: utf-8 -*-
'''
Created on  2017-11Nov-20
Modified on 2017-11Nov-20
Version 0.01.a
@author: rainier.madruga@gmail.com
A simple Python Program to randomly generate Reggaeton song lyrics.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2017-11-20       RWM        Initial Stub and Layout
'''

# Import Libraries needed for Scraping the various web pages
import random
import datetime

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Visual Spacing Elements for Parsing
hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

introLine = ["Mami", "Bebe", "Princesa", "¡Ay! Mami", "Niña", "Mi Corazon", "Mami"]
goalStmt = ["Yo Quiero", "Yo Puedo", "Yo Vengo A", "Voy A", "Quiero"]
actionStmt = ["Encenderte", "Amarte", "Ligar", "Jugar", "Enamorarte", "Llevarte al Cielo"]
descStmt = ["Suave", "Lento", "Rapido", "Fuerte", "Duro"]
duraStmt = ["Hasta Que Salga el Sol", "Todo la Noche", "Hasta el Amanecer", "Todo el Dia", "Vivir Por Siempre"]
emotStmt = ["Sin Ansiedad", "Sin Compromiso", "Feis to Feis", "Sin Miedo"]

intro = []
verseChorus = []
middle8 = []
chorus = []
outro = []

secure_random = random.SystemRandom()

def lyricGen (type):
    verseTyp = type
    lyric = ""
    partA = secure_random.choice(introLine)
    partB = secure_random.choice(goalStmt)
    partC = secure_random.choice(actionStmt)
    partD = secure_random.choice(descStmt)
    partE = secure_random.choice(duraStmt)
    partF = secure_random.choice(emotStmt)

    if verseTyp == "i":
        inSegA = [partA, partB, partC]
        # print (inSegA)
        lyric = inSegA
    if verseTyp == "v":
        inSegB = [partA, partB, partC, partD]
        # print (inSegB)
        lyric = inSegB
    if verseTyp == "c":
        inSegC = [partB, partC, partD, partE, partF]
        # print (inSegC)
        lyric = inSegC
    if verseTyp == 'o':
        inSegD = [partA, partC, partE, partF]
        # print (inSegD)
        lyric = inSegD
    if verseTyp == "h":
        inSegE = [partF, partB, partC]
    return lyric

def printLyrics (num, lyricCmpt):
    count = 0
    printVerse = num
    verseToPrint = lyricCmpt
    verse = ""
    while count <= num:
        # Print out Lyrics...
        for i in lyricCmpt:
            verse = verse + " " + i
        if 0 < num > count:
            verse = verse + ",\n"
        count += 1
    print (verse)

intro01 = lyricGen("i")
intro02 = lyricGen("i")
chorus = lyricGen("c")
verse01 = lyricGen("v")
verse02 = lyricGen("v")
hook = lyricGen("h")
verseChorus = chorus + verse01
outro = lyricGen("o")

printLyrics(0, intro01)
printLyrics(0, verse01)
printLyrics(0, intro02)
printLyrics(1, verseChorus)
printLyrics(0, verse01)
printLyrics(0, verse02)
printLyrics(0, verseChorus)
printLyrics(0, intro02)
printLyrics(0, chorus)
printLyrics(0, verse02)
printLyrics(0, verse01)
printLyrics(0, outro)