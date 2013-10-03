#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from collections import OrderedDict
import re
import cgi
from time import localtime, strftime
from brewerydb import *
import json
import sys
import config

# command line arg for
useAPI = True
if len(sys.argv) == 2:
    if sys.argv[1] == "-n":
        useAPI = False

# load novare beer list
response = urllib2.urlopen('http://novareresbiercafe.com/draught.php')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html)

# for storing the various categories of draughts
lists = OrderedDict() 
listTitles = [
    "On Draught",
    "Regular Draughts",
    "Regular Draughts:",
    "On Draught:",
    "On Tap",
    "Regular Draughts",           
    "Non Belgian Offerings", 
    "Maine Draughts",
    "Maine Draughts:",
    "Maine Beer Draughts",
    "Maine Taps",
    "On Cask",
    "On Draught",
    "Stout Fest Offerings"
]

# default index in case none listed/recognized
index = listTitles[0]
lists[index] = []

# configure brewerydb API
BreweryDb.configure(config.key)

# find all beers in the draughts_reg span
for beer in soup.find("span", "draughts_reg").find_all("p"):
    # get rid of tags in section header
    beer.string = beer.get_text()

    # do not display empty entries
    if beer.string != None and beer.string.strip() != "":
        beer.string = beer.string.strip()
        beer = beer.string.encode('utf-8')
        beer = beer.replace('’','\'')

        # create new list if a category heading detected
        if (beer in listTitles):
            index = beer
            lists[index] = []
        else:
            if useAPI == True:
                response = json.loads(BreweryDb.search({'type':'beer','q':beer}))
            if 'totalResults' in response:
                beerInfo = response['data'][0]
                beerInfo['novareName'] = beer
            else:
                beerInfo = {'novareName': beer}
            lists[index].append(beerInfo)
            
# output list as json with current timestamp
print json.dumps({
    'lists': lists,
    'timestamp': strftime("%m-%d-%Y %H:%M:%S", localtime())
})
