import requests
import json
import matplotlib.pyplot as plt
import threading
import changeDateParams as cdp
import copy
import re
import queue

STRIPPED = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

MAX_ARTICLES = 250

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

reqQueue = queue.Queue()

REQ_LOCK = threading.Lock()

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

NUM_COUNTRIES = 1
COUNTRIES = [['US', 'United States']]
COUNTRIES_LOCK.release()

def freqAdd(periodResults, collectVar, collectKey):
    collectVar[collectKey[0]][collectKey[1]] += len(periodResults['articles'])
    printMulti(f'testing {len(periodResults["articles"])} {collectVar}')
    return None

def granularReq(inURL, inPayload, searchRate, collectVar, collectLock, collectKey, processResults):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    REQ_LOCK.acquire()
    
    periodResp = requests.get(inURL, params=inPayload)
    try:
        periodResults = periodResp.json()
    except json.decoder.JSONDecodeError:
        firstStrip = re.sub('\\\\', '', periodResp.text)
        correctStr = STRIPPED(firstStrip)
        periodResults = json.loads(correctStr)
    
    REQ_LOCK.release()
    

    if (len(periodResults.keys()) != 0):
        periodArticles = len(periodResults['articles'])
        if periodArticles < MAX_ARTICLES:
            collectLock.acquire()
            processResults(periodResults, collectVar, collectKey)
            collectLock.release()
        else:
            if searchRate == 'monthly':
                granularSearch(inURL, inPayload, 'daily', collectVar, collectLock, collectKey, processResults)
            elif searchRate == 'daily':
                granularSearch(inURL, inPayload, 'hourly', collectVar, collectLock, collectKey, processResults)
            elif searchRate == 'hourly':
                granularSearch(inURL, inPayload, 'minute', collectVar, collectLock, collectKey, processResults)
    
    return None

def granularSearch(inURL, inPayload, searchRate, collectVar, collectLock, collectKey, processResults):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    start = inPayload['STARTDATETIME']
    loopEnd = 0

    if searchRate == 'yearly':
        #make monthly requests
    elif searchRate == 'monthly':
        # make daily requests
        month =  int(cdp.getMonth(start))
        loopEnd = MONTH_END[month]
        
    elif searchRate == 'daily':
        # make hourly requests
        loopEnd = 24

    elif searchRate == 'hourly':
        # make minute by minute requests
        loopEnd = 60

    for openThread in range(loopEnd):

        if searchRate == 'monthly':
            end = cdp.incrementDay(start, 1)
        elif searchRate == 'daily':
            end = cdp.incrementHour(start, 1)
        elif searchRate == 'hourly':
            end = cdp.incrementMin(start, 1)

        inPayload['ENDDATETIME'] = end
        
        start = end
        inPayload['STARTDATETIME'] = start

    
    return None

def gdeltReq(inURL, inPayload, searchRate, collectVar, collectLock, collectKey, processResults):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)


    """
    REQ_LOCK.acquire()

    resp = requests.get(inURL, params=inPayload)
    try:
        results = resp.json()
    except json.decoder.JSONDecodeError:
        firstStrip= re.sub('\\\\', '', resp.text)
        correctStr = STRIPPED(firstStrip)

        printMulti(correctStr)
        
        results = json.loads(correctStr)

    REQ_LOCK.release()
    
    
    if len(results.keys()) != 0:
        articles = len(results['articles'])
        if articles < MAX_ARTICLES:
            collectLock.acquire()
            processResults(results, collectVar, collectKey)
            collectLock.release()
        else:
            # perform a more granular search
            granularSearch(inURL, inPayload, searchRate, collectVar, collectLock, collectKey, processResults)

    """
    return None

def testG(inG, key):
    inG[key]['test1'] = 20
    inG[key]['test2'] = 35
    return None

def testingDict():

    testDict = {}
    testDict['tests'] = {}
    testG(testDict, 'tests')
    print(testDict)

    return None

PRINT_LOCK = threading.Lock()

def printMulti(strText):
    PRINT_LOCK.acquire()
    print(strText)
    PRINT_LOCK.release()
    return None

# testingDict()

COUNTRY_COUNTER_LOCK = threading.Lock()
COUNTRY_COUNTER = 0

gdeltAPI = 'https://api.gdeltproject.org/api/v2/doc/doc'

dataCollect = {}

COUNTRY_COUNTER_LOCK.acquire()
while (COUNTRY_COUNTER < NUM_COUNTRIES):

    countryIdx = COUNTRY_COUNTER
    COUNTRY_COUNTER += 1
    COUNTRY_COUNTER_LOCK.release()

    COUNTRIES_LOCK.acquire()
    countryCode = COUNTRIES[countryIdx][0]
    countryName = COUNTRIES[countryIdx][1]
    COUNTRIES_LOCK.release()
    printMulti(f'START: {countryName}')

    payload = {}
    payload['MODE'] = 'ArtList'
    payload['FORMAT'] = 'JSON'

    # Gets maximum allowed number of articles per request
    payload['MAXRECORDS'] = '250'

    # start date Feb 1 2020
    # date format YYYYMMDDHHMMSS
    dateStart = '20200201000000'
    dateEnd = cdp.incrementMonth(dateStart, 1)

    
    dataCollect[countryName] = [0, 'test1', 'test2']
    dataLock = threading.Lock()
    collectKey = (countryName, 0)

    for i in range(5):

        # Will only search through articles posted through dateStart-dateEnd
        payload['STARTDATETIME'] = dateStart
        payload['ENDDATETIME'] = dateEnd

        # runs search for query with seafood for this particular country
        payload['QUERY'] = 'seafood sourcecountry:' + countryCode

        searchRate = 'monthly'

        t0 = threading.Thread(target=gdeltReq, args=(gdeltAPI, payload, searchRate, dataCollect, dataLock, collectKey, freqAdd,))
        t0.start()

        # update start and end times
        dateStart = dateEnd
        dateEnd = cdp.incrementMonth(dateStart, 1)

        payload['STARTDATETIME'] = dateStart
        payload['ENDDATETIME'] = dateEnd

t0.join()

printMulti(dataCollect)
