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
COUNTRIES = [['CA', 'Canada']]
COUNTRIES_LOCK.release()

REQ_QUEUE = queue.Queue()
REQ_QUEUE_LOCK = threading.Lock()

# builds more granular searches and puts them on REQ_QUEUE
def granularSearch(inList):
    print('granular here')

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
        loopEnd = 60
        newSearchRate = 'minute'
    

    for loopStart in range(loopEnd):
        if searchRate == 'monthly':
            end = cdp.incrementDay(start, 1)
        elif searchRate == 'daily':
            end = cdp.incrementHour(start, 1)
        elif searchRate == 'hourly':
            end = cdp.incrementMin(start, 1)
        
        # creating new list for more granular search
        newReqList = copy.deepcopy(inList)
        newReqList[3] = start
        newReqList[4] = end
        newReqList[6] = newSearchRate

        # add new granular search to request queue
        print('before granular acquire')
        REQ_QUEUE_LOCK.acquire()
        print('putting somethign on the REQ_QUEUE')
        REQ_QUEUE.put(newReqList)
        REQ_QUEUE_LOCK.release()

        start = end

    print('ENDING GRANULAR')
    return None

# builds and sends the request from the variables in the REQ_QUEUE
# if the MAX_RESULTS are found put more granular searches in the REQ_QUEUE
def makeReq(inList):

    print('here')
    print(inList)
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
        print('exception handling')
        results = json.loads(correctStr)


    print('before article limit')
    print(f'len keys {len(results.keys())}')
    # checks to see if more granular searches are necessary or if results can be recorded
    if (len(results.keys()) > 0):
        articles = len(results['articles'])
        print(f'articles {articles}')
        if articles < MAX_ARTICLES:
            # do something with articles results
            print(f'num articles found {articles}')
        else:
            print('have to make a granular search')
            print(f'search rate {searchRate}')
            granularSearch(inList)

    print('ENDING MAKE REQ')
    return None

# takes requests off of the queue and calls to execute the request
def reqConsumer():

    REQ_QUEUE_LOCK.acquire()
    
    print('getting something from the REQ_QUEUE')
    newReq = REQ_QUEUE.get()
    REQ_QUEUE_LOCK.release()

    makeReq(newReq)

    return None


def mainRequester():
    
    REQ_QUEUE_LOCK.acquire()
    while not REQ_QUEUE.empty():
        REQ_QUEUE_LOCK.release()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(reqConsumer)
        
        REQ_QUEUE_LOCK.acquire()
    REQ_QUEUE_LOCK.release()
    return None

# ==================================================================================================
# SHOW CASE EXAMPLE


COUNTRIES_LOCK.acquire()
countryCode = COUNTRIES[0][0]
countryName = COUNTRIES[0][1]
COUNTRIES_LOCK.release()

reqMode = 'ArtList'
reqFormat = 'JSON'
articleCount = MAX_ARTICLES
startTime = '20200101000000'
endTime = '20200201000000'
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

REQ_QUEUE_LOCK.acquire()
REQ_QUEUE.put(reqList)
REQ_QUEUE_LOCK.release()

mainRequester()

REQ_QUEUE_LOCK.acquire()
print(REQ_QUEUE.qsize())
print()
while not REQ_QUEUE.empty():
    print(REQ_QUEUE.get())
REQ_QUEUE_LOCK.release()