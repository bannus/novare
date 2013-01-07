#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import cgi
from time import localtime, strftime
from brewerydb import *
import json

# load novare beer list
response = urllib2.urlopen('http://novareresbiercafe.com/draught.php')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html)
print '{'
print "beers: "

# configure brewerydb API
BreweryDb.configure("3e87654b8c90922e6fe4aaefa3e45a89")

# find all beers in the draughts_reg span
for beer in soup.find("span", "draughts_reg").find_all("p"):
    # do not display empty entries
    if beer.string != None and beer.string.strip() != "":
        beer = beer.string.encode('utf-8')
        if (beer == "Non Belgian Offerings" or beer == "Maine Draughts"):
            print "<heading>" +  beer + "</heading>"
        else:
            print "<beer>" + beer + "</beer>"
            #response = json.loads(BreweryDb.search({'type':'beer','q':beer}))
            json.dumps(response['data'][0])
            if 'totalResults' in response:
                beerInfo = response['data'][0]
                print beerInfo['name'].encode('utf-8')


print "<timestamp>"
print strftime("%m-%d-%Y %H:%M:%S", localtime())
print "</timestamp>"
print "</beers>"
