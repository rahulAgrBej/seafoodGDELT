# GDELT requester

import requests
import json
import matplotlib.pyplot as plt
import threading
import changeDateParams as cdp
import copy
import re
import queue

MAX_ARTICLES = 250
GDELT_API = 'https://api.gdeltproject.org/api/v2/doc/doc'

MONTH_END = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

STRIPPED = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

COUNTRIES = []
COUNTRIES_LOCK = threading.Lock()

COUNTRIES_LOCK.acquire()
# reads in all GDELT supported Countries
countryFile = open('supportedCountries.txt', 'r')
NUM_COUNTRIES = int(countryFile.readline().rstrip('\n'))
for cCount in range(NUM_COUNTRIES):
    line = countryFile.readline().rstrip('\n')
    countryData = line.split('\t')
    COUNTRIES.append(countryData)
countryFile.close()

# TEST EXAMPLE
COUNTRIES = [['CA', 'Canada']]
COUNTRIES_LOCK.release()

REQ_QUEUE = queue.Queue()

# builds and sends the request from the variables in the REQ_QUEUE
# if the MAX_RESULTS are found put more granular searches in the REQ_QUEUE
def makeReq(inList):

    # builds payload of parameters of query
    payload = {}
    payload['MODE'] = inList[0]
    payload['FORMAT'] = inList[1]
    payload['MAXRECORDS'] = inList[2]
    payload['STARTDATETIME'] = inList[3]
    payload['ENDDATETIME'] = inList[4]
    payload['QUERY'] = inList[5]

    # makes request
    resp = requests.get(GDELT_API, params=payload)
    
    # cleans results if necessary
    try:
        results = resp.json()
    except json.decoder.JSONDecodeError:
        firstStrip = re.sub('\\\\', '', resp.text)
        correctStr = STRIPPED(firstStrip)
        results = json.loads(correctStr)
    
    # checks to see if more granular searches are necessary or if results can be recorded
    if (len(results.keys()) != 0):
        articles = len(periodResults['articles'])
        if articles < MAX_ARTICLES:
            # do something with articles results
        else:
            if searchRate == 'monthly':
                granularSearch(inURL, inList, 'daily')
            elif searchRate == 'daily':
                granularSearch(inURL, inList, 'hourly')
            elif searchRate == 'hourly':
                granularSearch(inURL, inList, 'minute')

    return None


# ==================================================================================================
# SHOW CASE EXAMPLE

RESULTS = [[]]

for country in COUNTRIES:

    countryCode = country[0]
    countryName = country[1]

    reqMode = 'ArtList'
    reqFormat = 'JSON'
    articleCount = MAX_ARTICLES
    startTime = '20200101000000'
    endTime = '20200201000000'
    reqQuery = 'seafood sourcecountry:' + countryCode

    reqList = []
    reqList.append(reqMode)
    reqList.append(reqFormat)
    reqList.append(articleCount)
    reqList.append(startTime)
    reqList.append(endTime)
    reqList.append(reqQuery)
    reqList.append(RESULTS[0])