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
    "Draughts",
    "Regular Draughts",
    "Draught Bier",
    "Maine Draughts",
    "Maine Beer Draughts",
    "Maine Taps",
    "Cask",
    "On Draught",
    "On Tap",
    "On Cask",
    "Non Belgian Offerings",
    "Stout Fest Offerings",
    "Shelton Brother Draughts",
    "Shelton Brothers Draughts"
]
listTitles = listTitles + [title + ":" for title in listTitles]
listTitles = listTitles + [title.upper() for title in listTitles]

# configure brewerydb API
BreweryDb.configure(config.key)
index = None

# find all beers in the draughts_reg span
for beer in soup.find("span", "draughts_reg").find_all(["p", "h1", "h2", "h3", "h4"]):
    # get rid of tags in section header
    beer = beer.get_text()

    # do not display empty entries
    if beer != None and beer.strip() != "":
        beer = beer.strip()
        beer = beer.replace(u"\u00a0", " ")
        beer = beer.encode('utf-8')
        beer = beer.replace('’', '\'')

        # create new list if a category heading detected
        if (beer in listTitles):
            index = beer.title()
            lists[index] = []
        else:
            # default index in case none listed/recognized
            if index == None:
                index = listTitles[0]
                lists[index] = []
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
