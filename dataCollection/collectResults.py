import requests
import json
import matplotlib.pyplot as plt
import threading
from changeDateParams as cdp
import copy
import re

MAX_ARTICLES = 250

monthEnd = {
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

def granularSearch(inURL, inPayload, searchRate, collectVar, collectLock, collectKey, processResults):

    # otherwise alters payload variable that was passed into it
    inPayload = copy.deepcopy(inPayload)

    startPeriod = inPayload['STARTDATETIME']
    loopEnd = 0

    if searchRate == 'monthly':
        # make daily requests
        month =  int(cdp.getMonth(startDay))
        loopEnd = MONTH_END[month]
        
    elif searchRate == 'daily':
        # make hourly requests
        loopEnd = 24

    elif searchRate == 'hourly':
        # make minute by minute requests
        loopEnd = 60

    start = inPayload['STARTDATETIME']

    for i in range (loopEnd):

        if searchRate == 'monthly':
            end = cdp.incrementDay(start, 1)
        elif searchRate == 'daily':
            end = cdp.incrementHour(start, 1)
        elif searchRate == 'hourly':
            end = cdp.incrementMin(start, 1)

        inPayload['ENDDATETIME'] = end
        periodResp = requests.get(inURL, inPayload)
        try:
            periodResults = periodResp.json()
        except json.decoder.JSONDecodeError:
            firstStrip = re.sub('\\\\', '', periodResp.text)
            correctStr = STRIPPED(firstStrip)
            periodResults = json.loads(correctStr)

        if (len(periodResults.keys()) != 0):
            periodArticles = len(periodResults['articles'])
            if periodArticles < MAX_ARTICLES:
                collectLock.acquire()
                processResults(periodResults, collectVar, collectKey)
                collectLock.release()
            else:
                if searchRate == 'monthly':
                    granularSearch(inURL, inPayload, 'daily', collectVar, collectLocks, collectKey)
                elif searchRate == 'daily':
                    granularSearch(inURL, inPayload, 'hourly', collectVar, collectLocks, collectKey)
                elif searchRate == 'hourly':
                    granularSearch(inURL, inPayload, 'minute', collectVar, collectLocks, collectKey)
        
        start = end
        inPayload['STARTDATETIME'] = start
    
    return None

def gdeltReq(inURL, inPayload, searchRate, collectVar, collectLocks, collectKey, processResults):

    resp = requests.get(inURL, payload=inPayload)
    try:
        results = resp.json()
    except json.decoder.JSONDecodeError:
        firstStrip= re.sub('\\\\', '', resp.text)
        correctStr = STRIPPED(firstStrip)
        results = json.loads(correctStr)
    
    if len(results.keys()) != 0:
        articles = len(results['articles'])
        if articles < MAX_ARTICLES:
            collectLock.acquire()
            processResults(dailyResults, collectVar, collectKey)
            collectLock.release()
        else:
            # perform a more granular search
            granularSearch(inURL, inPayload, searchRate, collectVar, collectLocks, collectKey)

    return None

def testG(inG, key):
    inG[key] = 'PASSED'
    return None

def testingDict():

    testDict = {}
    testDict['tests'] = 'failed'
    testG(testDict, 'tests')
    print(testDict)

    return None

testingDict()