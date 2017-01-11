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
try:
    import config
except ImportError:
    print "You must specify the BreweryDb key in config.py as variable 'key'"
    sys.exit()

UPDATED = 0
LIST1_HEADING = 1
LIST1 = 2
LIST2_HEADING = 3
LIST2 = 4

# Strip whitespace, format spaces properly, replace curly quote
def process_text(text):
    return text.strip() \
            .strip() \
            .replace(u"\u00a0", " ") \
            .encode('utf-8') \
            .replace('’', '\'')

def process_list(input_list, output_list):
    for beer in input_list.find_all("p"):
        beer = beer.get_text()
        if beer != None and beer.strip() != "":
            beer = process_text(beer)
            if useAPI:
                response = json.loads(BreweryDb.search({'type':'beer','q':beer}))
                if 'totalResults' in response:
                    beerInfo = response['data'][0]
                    beerInfo['novareName'] = beer
            else:
                beerInfo = {'novareName': beer}
            output_list.append(beerInfo)

if __name__ == '__main__':
    # command line arg for
    useAPI = True
    if len(sys.argv) == 2:
        if sys.argv[1] == "-n":
            useAPI = False

    # load novare beer list
    response = urllib2.urlopen('http://novareresbiercafe.com/draught/')
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html)

    lists = OrderedDict()

    # configure brewerydb API
    BreweryDb.configure(config.key)
    index = None

    text_columns = soup.find_all("div", "wpb_text_column")

    # check if the first text column has the text 'updated.' if so,
    # we're good to go.
    if "updated" not in text_columns[0].text.lower():
        print "Novare Res site format changed, scraping failed. Call Bannus!"

    # init list 1 (probably "Regular Draughts"). convert to title casing
    list1_heading = process_text(text_columns[LIST1_HEADING].get_text()).title()
    lists[list1_heading] = []

    # build list 1
    process_list(text_columns[LIST1], lists[list1_heading])

    # init list 2 (probably "Maine Draughts"). convert to title casing
    list1_heading = process_text(text_columns[LIST2_HEADING].get_text()).title()
    lists[list1_heading] = []

    # build list 2
    process_list(text_columns[LIST2], lists[list1_heading])

    # output list as json with current timestamp
    print json.dumps({
        'lists': lists,
        'timestamp': strftime("%m-%d-%Y %H:%M:%S", localtime())
        })

