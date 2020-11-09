import json
import requests
import urllib.parse
from itertools import permutations, combinations

FREQ_API_URL = 'http://127.0.0.1:5000/api/searchTrends'

test = 'https://article-search-api.herokuapp.com/api/searchTrends'

MAIN_IDS = [
    {'id': 'US'},
    {'id': 'CH'},
    {'id': 'CA'}
    ]

MAIN_COUNTRIES = ['US', 'CH', 'CA']

# reads in all source countries into a dictionary with country id : country name
def readCountries():

    sourceCountries = {}

    f = open('countryLookUp.txt', 'r')
    data = f.readlines()
    f.close()

    for country in data:
        country = country.rstrip('\n')
        country = country.split('\t')
        sourceCountries[country[0]] = ' '.join(country[1:])

    return sourceCountries

# returns all possible combos of sourceCountries
def allCombos():
    combos = []

    sourceCountries = readCountries()
    ids = sourceCountries.keys()
    combos = combinations(ids, 2)

    return combos

def addReq(q, country, startDate, startTime, endDate, endTime):
    req = []
    req.append(q)
    req.append(country)
    req.append(startDate)
    req.append(startTime)
    req.append(endDate)
    req.append(endTime)
    return req

# gets all article counts for a specific query and combination of countries
def buildArticleCountsReqs(inQuery, combos, startDate, startTime, endDate, endTime):

    sourceCountries = readCountries()

    allReqs = []
    
    for combo in combos:
        query = f'\"{sourceCountries[combo[0]]}\" \"{sourceCountries[combo[1]]}\" ' + inQuery

        for mId in MAIN_IDS:
            req = addReq(query, mId, startDate, startTime, endDate, endTime)
            allReqs.append(req)

        if not (combo[0] in MAIN_COUNTRIES):
            req = addReq(query, {'id': combo[0]}, startDate, startTime, endDate, endTime)
            allReqs.append(req)

        
        if not (combo[1] in MAIN_COUNTRIES):
            req = addReq(query, {'id': combo[1]}, startDate, startTime, endDate, endTime)
            allReqs.append(req)
    
    payload = {}
    payload['requestsSent'] = allReqs
    encodedPayload = urllib.parse.urlencode()
    finalURL = FREQ_API_URL + "?" + encodedPayload
    resp = requests.get(finalURL)

    if resp.status_code == 200:
        data = resp.join()['results']
    else:
        print("ERROR")
        print(query)
        print(resp.content)
        data = []

    return allReqs

def sendCountReqs(reqs, batchSize):
    
    batch = []
    data = []

    for req in reqs:
        
        batch.append(req)

        if len(batch == batchSize):
            payload = {}
            payload['requestsSent'] = batch
            resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
            
            if resp.status_code == 200:
                responseResults = resp.json()["results"]
                for res in responseResults:
                    data.extend(res["articles"])
            
            batch = []
    
    if len(batch) > 0:
        payload = {}
        payload['requestsSent'] = batch
        resp = requests.get(ARTICLE_SEARCH_API + "?" + urllib.parse.urlencode(payload))
        
        if resp.status_code == 200:

            # CHECK TO SEE THE FORMAT FOR THIS
            responseResults = resp.json()["results"]
            for res in responseResults:
                data.extend(res)
    
    return data