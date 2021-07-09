import json
import requests
import urllib.parse
from itertools import permutations, combinations

FREQ_API_URL = 'https://article-search-api.herokuapp.com/api/searchTrends'

test = 'http://127.0.0.1:5000/api/searchTrends'

MAIN_IDS = [
    {'id': 'US'},
    {'id': 'CH'},
    {'id': 'CA'}
    ]

MAIN_COUNTRIES = ['US', 'CH', 'CA']

# reads in all source countries into a dictionary with country id : country name
def readCountries():

    sourceCountries = {}

    f = open('countryLookUp.csv', 'r')
    data = f.readlines()
    f.close()

    for country in data[1:]:
        country = country.rstrip('\n')
        country = country.split(',')

        if int(country[-1]) == 0:
            sourceCountries[country[0]] = country[1]

    return sourceCountries

def  country2Id():

    countries = {}
    f = open('countryLookUp.csv', 'r')
    data = f.readlines()
    f.close()

    for country in data[1:]:
        country = country.rstrip('\n')
        country = country.split(',')

        if int(country[-1]) == 0:
            countries[country[1]] = country[0]
    
    return countries

# returns all possible combos of sourceCountries
def allCombos():
    combos = []

    sourceCountries = readCountries()
    ids = sourceCountries.keys()
    combos = combinations(ids, 2)

    return combos

def combosUS():
    
    sourceCountries = readCountries()
    ids = sourceCountries.keys()

    pairsUS = []
    for id in ids:
        if id != 'US':
            pairsUS.append(('US', id))
    
    return pairsUS


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
        if len(sourceCountries[combo[0]]) < 5:
            sourceCountry0 = sourceCountries[combo[0]]
        else:
            sourceCountry0 = f'\"{sourceCountries[combo[0]]}\"'

        if len(sourceCountries[combo[1]]) < 5:
            sourceCountry1 = sourceCountries[combo[1]]
        else:
            sourceCountry1 = f'\"{sourceCountries[combo[1]]}\"'
        
        query = f'{sourceCountry0} {sourceCountry1} ' + inQuery

        for mId in MAIN_IDS:
            req = addReq(query, mId, startDate, startTime, endDate, endTime)
            allReqs.append(req)

        if not (combo[0] in MAIN_COUNTRIES):
            req = addReq(query, {'id': combo[0]}, startDate, startTime, endDate, endTime)
            allReqs.append(req)

        
        if not (combo[1] in MAIN_COUNTRIES):
            req = addReq(query, {'id': combo[1]}, startDate, startTime, endDate, endTime)
            allReqs.append(req)

    return allReqs

def sendCountReqs(reqs, batchSize):
    
    batch = []
    data = []

    for req in reqs:
        
        batch.append(req)

        if len(batch) == batchSize:
            payload = {}
            payload['requestsSent'] = json.dumps(batch)
            resp = requests.get(FREQ_API_URL + "?" + urllib.parse.urlencode(payload))

            print(batch)
            print(resp.status_code)
            
            if resp.status_code == 200:
                responseResults = resp.json()["results"]
                data.extend(responseResults)
            
            batch = []
    
    if len(batch) > 0:
        payload = {}
        payload['requestsSent'] = json.dumps(batch)
        resp = requests.get(FREQ_API_URL + "?" + urllib.parse.urlencode(payload))

        print(batch)
        print(resp.status_code)
        
        if resp.status_code == 200:

            # CHECK TO SEE THE FORMAT FOR THIS
            responseResults = resp.json()["results"]
            data.extend(responseResults)
        else:
            print("ERROR ERRROR ERROR")
    
    return data
