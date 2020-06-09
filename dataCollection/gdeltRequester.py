# GDELT requester

import requests
import json
import matplotlib.pyplot as plt
import threading
import changeDateParams as cdp
import copy
import re
import queue
import concurrent.futures

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
#COUNTRIES = [['US', 'United States']]
COUNTRIES_LOCK.release()

REQ_QUEUE = queue.Queue()
REQ_QUEUE_LOCK = threading.Lock()

# builds more granular searches and puts them on REQ_QUEUE
def granularSearch(inList):

    # collect start time
    start = inList[3]
    end = ''
    searchRate = inList[6]
    newSearchRate = ''

    loopEnd = 0
    loopStart = 0

    if searchRate == 'monthly':
        # make daily requests
        month =  int(cdp.getMonth(start))
        loopEnd = MONTH_END[month]
        newSearchRate = 'daily'
        
    elif searchRate == 'daily':
        # make hourly requests
        loopEnd = 24
        newSearchRate = 'hourly'

    elif searchRate == 'hourly':
        # make minute by minute requests
        loopEnd = 2
        newSearchRate = 'minute'
    

    for loopStart in range(loopEnd):
        if searchRate == 'monthly':
            end = cdp.incrementDay(start, 1)
        elif searchRate == 'daily':
            end = cdp.incrementHour(start, 1)
        elif searchRate == 'hourly':
            end = cdp.incrementMin(start, 30)
        
        # creating new list for more granular search
        newReqList = copy.deepcopy(inList)
        newReqList[3] = start
        newReqList[4] = end
        newReqList[6] = newSearchRate

        # add new granular search to request queue
        REQ_QUEUE_LOCK.acquire()
        REQ_QUEUE.put(newReqList)
        REQ_QUEUE_LOCK.release()

        start = end
    return None

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
    
    searchRate = inList[6]

    # makes request
    resp = requests.get(GDELT_API, params=payload)
    
    # cleans results if necessary
    try:
        results = resp.json()
    except json.decoder.JSONDecodeError:
        firstStrip = re.sub('\\\\', '', resp.text)
        correctStr = STRIPPED(firstStrip)
        try:
            results = json.loads(correctStr)
        except:
            print('exception handling')
            print(correctStr)
            print(f'start {inList[3]}')
            print(f'end {inList[4]}')
            return None

    # checks to see if more granular searches are necessary or if results can be recorded
    if (len(results.keys()) > 0):
        articles = len(results['articles'])
        if articles < MAX_ARTICLES:
            # do something with articles results
            print(f'FOUND {articles} {inList}')
        else:
            granularSearch(inList)
    return None

# takes requests off of the queue and calls to execute the request
def reqConsumer():

    REQ_QUEUE_LOCK.acquire()
    
    if not REQ_QUEUE.empty():
        newReq = REQ_QUEUE.get()
        REQ_QUEUE_LOCK.release()
        makeReq(newReq)

    REQ_QUEUE_LOCK.release()

    return None


def mainRequester():
    
    REQ_QUEUE_LOCK.acquire()
    while not REQ_QUEUE.empty():
        currNumReqs = REQ_QUEUE.qsize()
        REQ_QUEUE_LOCK.release()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            for i in range(currNumReqs):
                executor.submit(reqConsumer)
        
        REQ_QUEUE_LOCK.acquire()
    REQ_QUEUE_LOCK.release()
    return None

# ==================================================================================================
# SHOW CASE EXAMPLE

REQ_QUEUE_LOCK.acquire()

for country in COUNTRIES:
    countryCode = country[0]
    countryName = country[1]
    startTime = '20200101000000'
    for i in range(5):
        reqMode = 'ArtList'
        reqFormat = 'JSON'
        articleCount = MAX_ARTICLES
        
        endTime = cdp.incrementMonth(startTime, 1)
        reqQuery = 'seafood sourcecountry:' + countryCode
        searchRate = 'monthly'

        reqList = []
        reqList.append(reqMode)
        reqList.append(reqFormat)
        reqList.append(articleCount)
        reqList.append(startTime)
        reqList.append(endTime)
        reqList.append(reqQuery)
        reqList.append(searchRate)
        REQ_QUEUE.put(reqList)

        startTime = endTime
REQ_QUEUE_LOCK.release()

mainRequester()
