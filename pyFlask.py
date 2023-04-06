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

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/greet')
def say_hello():
    return 'Hello from Server'